from oarepo_model_builder.stack.schema import model_paths


def path_valid(*path):
    ms = model_paths
    for p in path:
        ms = ms.get(p)
    return ms.valid


def test_is_schema_element():
    assert path_valid("type")
    assert path_valid("$id")
    assert path_valid("$schema")
    assert path_valid("properties")
    assert path_valid("properties", "a")
    assert path_valid("properties", "a", "type")
    assert path_valid("properties", "a", "items")
    assert path_valid("properties", "a", "items", "type")
    assert path_valid("properties", "a", "properties")

    assert not path_valid("test")
    assert not path_valid("blah", "properties", "a", "test")
