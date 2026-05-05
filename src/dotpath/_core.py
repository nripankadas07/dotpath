"""Core dotpath implementation."""
from __future__ import annotations

from typing import Any, Iterator, List, Sequence

__all__ = [
    "DotPathError",
    "delete",
    "get",
    "has",
    "join_path",
    "paths",
    "set_",
    "split_path",
]


class DotPathError(ValueError):
    """Raised on invalid paths or unsupported container types."""


_MISSING = object()


def split_path(path: str) -> List[str]:
    """Split a dotted path into segments. ``\\.`` is an escaped dot."""
    if not isinstance(path, str):
        raise DotPathError(f"path must be str, got {type(path).__name__}")
    if path == "":
        return []
    out: List[str] = []
    cur: List[str] = []
    i = 0
    while i < len(path):
        c = path[i]
        if c == "\\" and i + 1 < len(path) and path[i + 1] == ".":
            cur.append(".")
            i += 2
            continue
        if c == ".":
            out.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    out.append("".join(cur))
    if any(seg == "" for seg in out):
        raise DotPathError(f"empty segment in path {path!r}")
    return out


def join_path(segments: Sequence[str]) -> str:
    """Join segments back into a dotted path with proper escaping."""
    return ".".join(s.replace(".", "\\.") for s in segments)


def _step(container: Any, segment: str) -> Any:
    if isinstance(container, dict):
        if segment in container:
            return container[segment]
        return _MISSING
    if isinstance(container, list):
        try:
            idx = int(segment)
        except ValueError:
            return _MISSING
        if -len(container) <= idx < len(container):
            return container[idx]
        return _MISSING
    return _MISSING


def get(obj: Any, path: str, default: Any = _MISSING) -> Any:
    """Read the value at ``path``, returning ``default`` if missing.

    With no ``default`` and a missing path, raises :class:`DotPathError`.
    """
    cur = obj
    for seg in split_path(path):
        cur = _step(cur, seg)
        if cur is _MISSING:
            if default is _MISSING:
                raise DotPathError(f"path not found: {path!r}")
            return default
    return cur


def has(obj: Any, path: str) -> bool:
    """Return True if ``path`` resolves to a value."""
    sentinel = object()
    return get(obj, path, default=sentinel) is not sentinel


def set_(obj: Any, path: str, value: Any) -> None:
    """Set the value at ``path``, creating intermediate dicts as needed.

    Lists are not auto-created — to set a list element you must point at
    an existing list. Out-of-range indices raise :class:`DotPathError`.
    """
    segs = split_path(path)
    if not segs:
        raise DotPathError("cannot set on empty path")
    cur = obj
    for seg in segs[:-1]:
        nxt = _step(cur, seg)
        if nxt is _MISSING:
            if isinstance(cur, dict):
                cur[seg] = {}
                nxt = cur[seg]
            else:
                raise DotPathError(
                    f"cannot create nested key {seg!r} inside {type(cur).__name__}"
                )
        cur = nxt
    last = segs[-1]
    if isinstance(cur, dict):
        cur[last] = value
    elif isinstance(cur, list):
        try:
            idx = int(last)
        except ValueError:
            raise DotPathError(f"list index {last!r} is not an integer") from None
        if -len(cur) <= idx < len(cur):
            cur[idx] = value
        else:
            raise DotPathError(f"list index {idx} out of range for length {len(cur)}")
    else:
        raise DotPathError(f"cannot set on {type(cur).__name__}")


def delete(obj: Any, path: str) -> None:
    """Remove the value at ``path``. Raises if the path is missing."""
    segs = split_path(path)
    if not segs:
        raise DotPathError("cannot delete on empty path")
    cur = obj
    for seg in segs[:-1]:
        nxt = _step(cur, seg)
        if nxt is _MISSING:
            raise DotPathError(f"path not found: {path!r}")
        cur = nxt
    last = segs[-1]
    if isinstance(cur, dict):
        if last not in cur:
            raise DotPathError(f"path not found: {path!r}")
        del cur[last]
    elif isinstance(cur, list):
        try:
            idx = int(last)
        except ValueError:
            raise DotPathError(f"list index {last!r} is not an integer") from None
        if not (-len(cur) <= idx < len(cur)):
            raise DotPathError(f"list index {idx} out of range")
        del cur[idx]
    else:
        raise DotPathError(f"cannot delete on {type(cur).__name__}")


def paths(obj: Any, prefix: str = "") -> Iterator[str]:
    """Yield every leaf path in ``obj``, depth-first.

    Containers (dicts, lists) are recursed into. Anything else is a leaf.
    """
    if isinstance(obj, dict):
        if not obj:
            if prefix:
                yield prefix
            return
        for k, v in obj.items():
            seg = str(k).replace(".", "\\.")
            child = f"{prefix}.{seg}" if prefix else seg
            yield from paths(v, child)
    elif isinstance(obj, list):
        if not obj:
            if prefix:
                yield prefix
            return
        for i, v in enumerate(obj):
            child = f"{prefix}.{i}" if prefix else str(i)
            yield from paths(v, child)
    else:
        if prefix:
            yield prefix
