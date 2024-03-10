import json5

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.loaders.extend import (
    extend_modify_marshmallow,
    extract_extended_record,
    post_extend_modify_marshmallow,
)
from oarepo_model_builder.schema.schema import ModelSchema


def test_extend_marshmallow():
    fs = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(
        profile="record",
        filesystem=fs,
    )

    model = ModelSchema(
        "/tmp/test.json",  # NOSONAR: this is just a dummy path
        content=extension_model,
        included_models={"extended-model": lambda parent_schema: extended_model},
        reference_processors={
            ModelSchema.EXTEND_KEYWORD: [
                extract_extended_record,
                extend_modify_marshmallow,
            ]
        },
        post_reference_processors={
            ModelSchema.EXTEND_KEYWORD: [
                post_extend_modify_marshmallow,
            ]
        },
    )
    builder.build(model, "record", ["record"], "")

    loaded_model = json5.loads(fs.read("test/models/records.json"))
    assert loaded_model["model"]["marshmallow"] == {
        "base-classes": ["marshmallow.Schema"],
        "class": "aaa.BlahSchema",
        "extra-code": "",
        "generate": False,
        "module": "test.services.records.schema",
    }
    assert loaded_model["model"]["ui"]["marshmallow"] == {
        "base-classes": ["oarepo_runtime.services.schema.ui.InvenioUISchema"],
        "class": "aaa.BlahUISchema",
        "extra-code": "",
        "generate": False,
        "imports": [],
        "module": "test.services.records.ui_schema",
    }
    # assert that "a" is read & write false
    property_a = loaded_model["model"]["properties"]["metadata"]["properties"]["a"]
    assert property_a["marshmallow"]["read"] is False
    assert property_a["marshmallow"]["write"] is False
    assert property_a["ui"]["marshmallow"]["read"] is False
    assert property_a["ui"]["marshmallow"]["write"] is False

    service_config = fs.read("test/services/records/config.py")
    print(service_config)
    assert "from aaa import BlahSchema" in service_config
    assert "schema = BlahSchema" in service_config


def test_extend_with_extra_props():
    fs = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(
        profile="record",
        filesystem=fs,
    )

    model = ModelSchema(
        "/tmp/test.json",  # NOSONAR: this is just a dummy path
        content=extension_model_with_extra_props,
        included_models={"extended-model": lambda parent_schema: extended_model},
        reference_processors={
            ModelSchema.EXTEND_KEYWORD: [
                extract_extended_record,
                extend_modify_marshmallow,
            ]
        },
        post_reference_processors={
            ModelSchema.EXTEND_KEYWORD: [
                post_extend_modify_marshmallow,
            ]
        },
    )
    builder.build(model, "record", ["record"], "")

    loaded_model = json5.loads(fs.read("test/models/records.json"))
    assert loaded_model["model"]["marshmallow"] == {
        "base-classes": ["aaa.BlahSchema"],
        "class": "test.services.records.schema.TestSchema",
        "extra-code": "",
        "generate": True,
        "module": "test.services.records.schema",
    }
    assert loaded_model["model"]["ui"]["marshmallow"] == {
        "base-classes": ["aaa.BlahUISchema"],
        "class": "test.services.records.ui_schema.TestUISchema",
        "extra-code": "",
        "generate": True,
        "imports": [],
        "module": "test.services.records.ui_schema",
    }
    # assert that "a" is read & write false
    property_a = loaded_model["model"]["properties"]["metadata"]["properties"]["a"]
    assert property_a["marshmallow"]["read"] is False
    assert property_a["marshmallow"]["write"] is False
    assert property_a["ui"]["marshmallow"]["read"] is False
    assert property_a["ui"]["marshmallow"]["write"] is False

    service_config = fs.read("test/services/records/config.py")
    print(service_config)
    assert "from test.services.records.schema import TestSchema" in service_config
    assert "schema = TestSchema" in service_config

    schema = fs.read("test/services/records/schema.py")
    print(schema)

    assert "from aaa import BlahSchema" in schema
    assert "from aaa import BlahMetadataSchema" in schema
    assert "class TestSchema(BlahSchema)" in schema
    assert "metadata = ma_fields.Nested(lambda: TestMetadataSchema())" in schema
    assert "class TestMetadataSchema(BlahMetadataSchema)" in schema
    assert "b = ma_fields.String()" in schema


def test_extend_with_extra_props_inside_use():
    fs = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(
        profile="record",
        filesystem=fs,
    )

    model = ModelSchema(
        "/tmp/test.json",  # NOSONAR: this is just a dummy path
        content=extension_model_with_extra_props_inside_use,
        included_models={
            "extended-model": lambda parent_schema: extended_model,
            "used-model": lambda parent_schema: used_model,
        },
        reference_processors={
            ModelSchema.EXTEND_KEYWORD: [
                extract_extended_record,
                extend_modify_marshmallow,
            ]
        },
        post_reference_processors={
            ModelSchema.EXTEND_KEYWORD: [
                post_extend_modify_marshmallow,
            ]
        },
    )
    builder.build(model, "record", ["record"], "")

    loaded_model = json5.loads(fs.read("test/models/records.json"))
    assert loaded_model["model"]["marshmallow"] == {
        "base-classes": ["aaa.BlahSchema"],
        "class": "test.services.records.schema.TestSchema",
        "extra-code": "",
        "generate": True,
        "module": "test.services.records.schema",
    }
    assert loaded_model["model"]["ui"]["marshmallow"] == {
        "base-classes": ["aaa.BlahUISchema"],
        "class": "test.services.records.ui_schema.TestUISchema",
        "extra-code": "",
        "generate": True,
        "imports": [],
        "module": "test.services.records.ui_schema",
    }
    # assert that "a" is read & write false
    property_a = loaded_model["model"]["properties"]["metadata"]["properties"]["a"]
    assert property_a["marshmallow"]["read"] is False
    assert property_a["marshmallow"]["write"] is False
    assert property_a["ui"]["marshmallow"]["read"] is False
    assert property_a["ui"]["marshmallow"]["write"] is False

    service_config = fs.read("test/services/records/config.py")
    print(service_config)
    assert "from test.services.records.schema import TestSchema" in service_config
    assert "schema = TestSchema" in service_config

    schema = fs.read("test/services/records/schema.py")
    print(schema)

    assert "from aaa import BlahSchema" in schema
    assert "from aaa import BlahMetadataSchema" in schema
    assert "class TestSchema(BlahSchema)" in schema
    assert "metadata = ma_fields.Nested(lambda: TestMetadataSchema())" in schema
    assert "class TestMetadataSchema(BlahMetadataSchema)" in schema
    assert "b = ma_fields.String()" in schema


extension_model = {
    "record": {
        "module": {"qualified": "test"},
        "extend": "extended-model",
        "properties": {"metadata": {"properties": {}}},
    },
    "settings": {
        "python": {"use-black": False, "use-isort": False, "use-autoflake": False}
    },
}

extension_model_with_extra_props = {
    "record": {
        "module": {"qualified": "test"},
        "extend": "extended-model",
        "properties": {"metadata": {"properties": {"b": {"type": "keyword"}}}},
    },
    "settings": {
        "python": {"use-black": False, "use-isort": False, "use-autoflake": False}
    },
}

extension_model_with_extra_props_inside_use = {
    "record": {
        "module": {"qualified": "test"},
        "extend": "extended-model",
        "properties": {"metadata": {"properties": {"use": "used-model"}}},
    },
    "settings": {
        "python": {"use-black": False, "use-isort": False, "use-autoflake": False}
    },
}

used_model = {
    "b": {"type": "keyword"},
}


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
