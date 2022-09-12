from oarepo_model_builder.utils.deepmerge import deepmerge


def test_merge_simple():
    assert deepmerge(1, 2, []) == 1


def test_merge_dict():
    assert deepmerge(dict(a=1), dict(b=2), []) == dict(a=1, b=2)
    assert deepmerge(dict(a=1), dict(a=2), []) == dict(a=1)

    assert deepmerge(dict(a=dict(a=1)), dict(a=dict(a=2)), []) == dict(a=dict(a=1))
    assert deepmerge(dict(a=dict(a=1)), dict(a=dict(b=2), c=3), []) == dict(
        a=dict(a=1, b=2), c=3
    )


def test_merge_list():
    assert deepmerge([1, 2], [3, 4], []) == [1, 2]
    assert deepmerge([1, 2], [3, 4, 5], []) == [1, 2, 5]


def test_merge_list_dict():
    assert deepmerge([dict(a=1)], [dict(b=1)], []) == [dict(a=1, b=1)]
