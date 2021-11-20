from oarepo_model_builder.utils.schema import model_paths


def path_valid(*path):
    ms = model_paths
    for p in path:
        ms = ms.get(p)
    return ms.valid


def test_is_schema_element():
    assert path_valid('model')
    assert path_valid('model', 'type')
    assert path_valid('model', '$id')
    assert path_valid('model', '$schema')
    assert path_valid('model', 'properties')
    assert path_valid('model', 'properties', 'a')
    assert path_valid('model', 'properties', 'a', 'type')
    assert path_valid('model', 'properties', 'a', 'items')
    assert path_valid('model', 'properties', 'a', 'items', 'type')
    assert path_valid('model', 'properties', 'a', 'properties')

    assert not path_valid('test')
    assert not path_valid('model', 'test')
    assert not path_valid('model', 'properties', 'a', 'test')
