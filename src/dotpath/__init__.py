"""dotpath — dotted-key get/set/has/del over nested dicts and lists.

Public API:

* :func:`get`     — read a value at ``"a.b.0.c"`` (default if missing).
* :func:`set_`    — set a value at a path, creating intermediate dicts.
* :func:`has`     — does the path exist?
* :func:`delete`  — remove a key (or list index) at a path.
* :func:`paths`   — list every leaf path in an object.
* :func:`split_path` / :func:`join_path` — escape-aware path helpers.
* :class:`DotPathError` — raised for invalid paths or types.

Path syntax: dotted keys, with integer indices for list access.
``"users.0.name"`` reads ``obj["users"][0]["name"]``. Escape literal
``.`` in a key with ``\\.``.
"""
from __future__ import annotations

from ._core import (
    DotPathError,
    delete,
    get,
    has,
    join_path,
    paths,
    set_,
    split_path,
)

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

__version__ = "0.1.0"
