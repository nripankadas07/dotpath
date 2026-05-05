"""Tests for dotpath."""
import pytest

from dotpath import (
    DotPathError, delete, get, has, join_path, paths, set_, split_path,
)


class TestSplitJoin:
    def test_simple(self):
        assert split_path("a.b.c") == ["a", "b", "c"]

    def test_single(self):
        assert split_path("a") == ["a"]

    def test_empty(self):
        assert split_path("") == []

    def test_escaped_dot(self):
        assert split_path(r"a.b\.c.d") == ["a", "b.c", "d"]

    def test_join(self):
        assert join_path(["a", "b", "c"]) == "a.b.c"
        assert join_path(["a", "b.c"]) == r"a.b\.c"

    def test_round_trip(self):
        for segs in [["a"], ["a", "b"], ["with.dot", "ok"], ["x", "y", "z"]]:
            assert split_path(join_path(segs)) == segs

    def test_empty_segment_rejected(self):
        with pytest.raises(DotPathError):
            split_path("a..b")


class TestGet:
    def test_simple(self):
        d = {"a": {"b": 1}}
        assert get(d, "a.b") == 1

    def test_list_index(self):
        d = {"users": [{"name": "alice"}, {"name": "bob"}]}
        assert get(d, "users.1.name") == "bob"

    def test_negative_list_index(self):
        d = {"items": [10, 20, 30]}
        assert get(d, "items.-1") == 30

    def test_missing_default(self):
        assert get({"a": 1}, "b", default="missing") == "missing"

    def test_missing_no_default_raises(self):
        with pytest.raises(DotPathError):
            get({"a": 1}, "b")

    def test_index_out_of_range(self):
        d = {"items": [1, 2]}
        assert get(d, "items.5", default=None) is None


class TestHas:
    def test_present(self):
        assert has({"a": {"b": 1}}, "a.b") is True

    def test_missing(self):
        assert has({"a": 1}, "a.b") is False

    def test_list_present(self):
        assert has({"items": [1, 2]}, "items.0") is True

    def test_list_missing(self):
        assert has({"items": [1, 2]}, "items.5") is False


class TestSet:
    def test_simple(self):
        d = {}
        set_(d, "a.b.c", 42)
        assert d == {"a": {"b": {"c": 42}}}

    def test_overwrite(self):
        d = {"a": 1}
        set_(d, "a", 2)
        assert d == {"a": 2}

    def test_list_index(self):
        d = {"items": [1, 2, 3]}
        set_(d, "items.1", 99)
        assert d == {"items": [1, 99, 3]}

    def test_list_index_out_of_range(self):
        d = {"items": [1]}
        with pytest.raises(DotPathError):
            set_(d, "items.5", 99)

    def test_empty_path(self):
        with pytest.raises(DotPathError):
            set_({}, "", 1)


class TestDelete:
    def test_simple(self):
        d = {"a": {"b": 1, "c": 2}}
        delete(d, "a.b")
        assert d == {"a": {"c": 2}}

    def test_list_index(self):
        d = {"items": [1, 2, 3]}
        delete(d, "items.1")
        assert d == {"items": [1, 3]}

    def test_missing(self):
        with pytest.raises(DotPathError):
            delete({"a": 1}, "b")

    def test_missing_nested(self):
        with pytest.raises(DotPathError):
            delete({"a": {"b": 1}}, "a.c")


class TestPaths:
    def test_flat(self):
        assert sorted(paths({"a": 1, "b": 2})) == ["a", "b"]

    def test_nested(self):
        out = sorted(paths({"a": {"b": {"c": 1}}}))
        assert out == ["a.b.c"]

    def test_list_in_dict(self):
        out = sorted(paths({"items": [10, 20, 30]}))
        assert out == ["items.0", "items.1", "items.2"]

    def test_escapes_dot_in_key(self):
        out = list(paths({"a.b": 1}))
        assert out == [r"a\.b"]
