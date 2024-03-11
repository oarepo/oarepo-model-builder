from oarepo_model_builder.loaders.extend import (
    contains_only_inherited_properties,
    contains_only_non_inherited_properties,
    extend_modify_marshmallow,
    find_extend_roots,
    modify_object_marshmallow,
)
from oarepo_model_builder.schema.loader import SchemaLoader
from oarepo_model_builder.schema.value import ReferenceType, Source


def test_simple_loader(loaders):
    loader = SchemaLoader(loaders, {})
    data = loader.load(
        Source.create("simple.json", ReferenceType.NONE, content={"a": 1})
    )
    assert data.dump() == {"a": 1}


def test_include(loaders):
    loader = SchemaLoader(loaders, {"incl": lambda x: {"a": 1}})
    data = loader.load(
        Source.create("include.json", ReferenceType.NONE, content={"$ref": "incl"})
    )
    assert data.dump() == {"a": 1}
    assert len(data["a"].source) == 2

    data = loader.load(
        Source.create("include.json", ReferenceType.NONE, content={"use": "incl"})
    )
    assert data.dump() == {"a": 1}
    assert data.source.reference_type == ReferenceType.NONE
    assert data["a"].source.reference_type == ReferenceType.USE

    data = loader.load(
        Source.create("include.json", ReferenceType.NONE, content={"extend": "incl"})
    )
    assert data.dump() == {"a": 1}
    assert data["a"].source.reference_type == ReferenceType.EXTEND


def test_double_include(loaders):
    loader = SchemaLoader(
        loaders, {"incl": lambda x: {"a": 1}, "incl1": lambda x: {"a": {"use": "incl"}}}
    )
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"b": {"$ref": "incl1"}}
        )
    )
    assert data.dump() == {"b": {"a": {"a": 1}}}


def test_override(loaders):
    loader = SchemaLoader(loaders, {"incl": lambda x: {"a": 1}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": 2}
        )
    )
    assert data.dump() == {"a": 2}


def test_merge_arrays(loaders):
    loader = SchemaLoader(loaders, {"incl": lambda x: {"a": [1, 2]}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # prepend
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "<a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # append
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", ">a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}

    # included says append
    loader = SchemaLoader(loaders, {"incl": lambda x: {">a": [1, 2]}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # included says append, including prepend
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "<a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # included says append, including append => including wins
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", ">a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}

    # included says prepend
    loader = SchemaLoader(loaders, {"incl": lambda x: {"<a": [1, 2]}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}

    # included says prepend, including prepend => including wins
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "<a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # included says prepend, including append
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", ">a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}


def test_extend_roots(loaders):
    loader = SchemaLoader(
        loaders,
        {
            "incl": lambda x: {"a": 1, "b": 2},
            "incl1": lambda x: {"use": "incl", "d": 4},
        },
    )
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"extend": "incl1", "a": 3}
        )
    )
    assert data.dump() == {"a": 3, "b": 2, "d": 4}
    assert data["a"].source.reference_type == ReferenceType.NONE
    assert data["b"].source.reference_type == ReferenceType.USE
    assert data["b"].source.previous.reference_type == ReferenceType.EXTEND
    assert data["d"].source.reference_type == ReferenceType.EXTEND


def test_extend_preprocessor_only_inherited(loaders):
    data = _get_data_with_extension(loaders)
    roots = find_extend_roots(data)
    assert len(roots) == 1
    root = next(iter(roots))
    assert (
        contains_only_inherited_properties(root["properties"]["metadata"], {}) == True
    )
    assert (
        contains_only_non_inherited_properties(root["properties"]["metadata"], {})
        == False
    )
    modify_object_marshmallow(root, {})
    assert root.dump() == {
        "marshmallow": {"base-classes": ["aaa.BlahSchema"], "generate": True},
        "module": {"qualified": "test"},
        "properties": {
            "metadata": {
                "marshmallow": {"class": "aaa.BlahMetadataSchema", "generate": False},
                "properties": {
                    "a": {
                        "marshmallow": {"read": False, "write": False},
                        "type": "keyword",
                        "ui": {"marshmallow": {"read": False, "write": False}},
                    }
                },
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "class": "aaa.BlahMetadataUISchema",
                        "generate": False,
                    }
                },
            }
        },
        "ui": {"marshmallow": {"base-classes": ["aaa.BlahUISchema"], "generate": True}},
    }


def test_extend_preprocessor_only_inherited_arrays(loaders):
    data = _get_data_with_extension(
        loaders,
        extended_model={
            "marshmallow": {"class": "aaa.BlahSchema"},
            "ui": {"marshmallow": {"class": "aaa.BlahUISchema"}},
            "properties": {
                "metadata": {
                    "type": "object",
                    "marshmallow": {"class": "aaa.BlahMetadataSchema"},
                    "ui": {"marshmallow": {"class": "aaa.BlahMetadataUISchema"}},
                    "properties": {"a": {"type": "keyword", "arr": [1, 2, 3]}},
                }
            },
        },
    )
    extend_modify_marshmallow(data)
    assert data.dump()["record"] == {
        "marshmallow": {"base-classes": ["aaa.BlahSchema"], "generate": True},
        "module": {"qualified": "test"},
        "properties": {
            "metadata": {
                "marshmallow": {"class": "aaa.BlahMetadataSchema", "generate": False},
                "properties": {
                    "a": {
                        "marshmallow": {"read": False, "write": False},
                        "type": "keyword",
                        "arr": [1, 2, 3],
                        "ui": {"marshmallow": {"read": False, "write": False}},
                    }
                },
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "class": "aaa.BlahMetadataUISchema",
                        "generate": False,
                    }
                },
            }
        },
        "ui": {"marshmallow": {"base-classes": ["aaa.BlahUISchema"], "generate": True}},
    }


def test_extend_preprocessor_only_inherited_schema_arrays(loaders):
    data = _get_data_with_extension(
        loaders,
        extended_model={
            "marshmallow": {"class": "aaa.BlahSchema"},
            "ui": {"marshmallow": {"class": "aaa.BlahUISchema"}},
            "properties": {
                "metadata": {
                    "type": "object",
                    "marshmallow": {"class": "aaa.BlahMetadataSchema"},
                    "ui": {"marshmallow": {"class": "aaa.BlahMetadataUISchema"}},
                    "properties": {
                        "a": {"type": "array", "items": {"type": "keyword"}}
                    },
                }
            },
        },
    )
    extend_modify_marshmallow(data)
    assert data.dump()["record"] == {
        "marshmallow": {"base-classes": ["aaa.BlahSchema"], "generate": True},
        "module": {"qualified": "test"},
        "properties": {
            "metadata": {
                "marshmallow": {"class": "aaa.BlahMetadataSchema", "generate": False},
                "properties": {
                    "a": {
                        "items": {
                            "marshmallow": {"read": False, "write": False},
                            "type": "keyword",
                            "ui": {"marshmallow": {"read": False, "write": False}},
                        },
                        "type": "array",
                    }
                },
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "class": "aaa.BlahMetadataUISchema",
                        "generate": False,
                    }
                },
            }
        },
        "ui": {"marshmallow": {"base-classes": ["aaa.BlahUISchema"], "generate": True}},
    }


def _get_data_with_extension(loaders, main_schema=None, extended_model=None):
    if not extended_model:
        extended_model = {
            "marshmallow": {"class": "aaa.BlahSchema"},
            "ui": {"marshmallow": {"class": "aaa.BlahUISchema"}},
            "properties": {
                "metadata": {
                    "type": "object",
                    "marshmallow": {"class": "aaa.BlahMetadataSchema"},
                    "ui": {"marshmallow": {"class": "aaa.BlahMetadataUISchema"}},
                    "properties": {"a": {"type": "keyword"}},
                }
            },
        }
    if not main_schema:
        main_schema = {
            "record": {
                "module": {"qualified": "test"},
                "extend": "extended-model",
                "properties": {"metadata": {"properties": {}}},
            },
            "settings": {
                "python": {
                    "use-black": False,
                    "use-isort": False,
                    "use-autoflake": False,
                }
            },
        }

    loader = SchemaLoader(
        loaders,
        {"extended-model": lambda x: extended_model},
    )
    data = loader.load(
        Source.create(
            "include.json",
            ReferenceType.NONE,
            content=main_schema,
        )
    )
    return data
