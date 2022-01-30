from oarepo_model_builder.utils.json_pathlib import JSONPaths, PathCondition


def test_condition():
    current = PathCondition(start={"a": {"b": 1}})
    assert current.a.b._subtree_list == [1]

    assert current.a.b == 1
    assert not (current.a.b == 2)
    assert current.a.b != 2


def test_condition_star():
    current = PathCondition(start={"a": {"b": 1, "c": 2}})
    assert current.a["*"]._subtree_list == [1, 2]

    assert current.a["*"] == 1
    assert current.a["*"] == 2
    assert current.a["*"] != 3


def test_condition_double_star():
    current = PathCondition(start={"a": {"b": 1, "c": {"d": 2}}})
    assert current.a["**"]._subtree_list == [1, {"d": 2}, 2]


def test_path_simple():
    p = JSONPaths()
    p.register(path="/a/b", value=1)
    assert list(p.match("/a/b")) == [1]
    assert list(p.match("/a")) == []


def test_path_locator():
    p = JSONPaths()
    p.register(path="/a/b", condition=lambda current: current.a == 1, value=1)
    assert list(p.match("/a/b", {"a": 1})) == [1]
    assert list(p.match("/a/b", {"a": 2})) == []


def test_path_multiple_locators():
    p = JSONPaths()
    p.register(path="/a/b", condition=lambda current: current.a == 1, value=1)
    p.register(path="/a/b", condition=lambda current: current.b == 1, value=2)
    assert list(p.match("/a/b", {"a": 1})) == [1]
    assert list(p.match("/a/b", {"b": 1})) == [2]
    assert list(p.match("/a/b", {"a": 1, "b": 1})) == [1, 2]
    assert list(p.match("/a/b", {"a": 2})) == []
