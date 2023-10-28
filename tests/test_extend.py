import json5

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.loaders.extend import (
    extend_modify_marshmallow,
    extract_extended_record,
)
from oarepo_model_builder.schema import ModelSchema


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
    )
    builder.build(model, "record", ["record"], "")

    loaded_model = json5.loads(fs.read("test/models/records.json"))
    assert loaded_model["model"]["marshmallow"] == {
        "base-classes": ["aaa.BlahSchema"],
        "class": "test.services.records.schema.TestSchema",
        "extra-code": "",
        "generate": True,
        "imports": [{"alias": "aaa", "import": "aaa"}],
        "module": "test.services.records.schema",
    }
    assert loaded_model["model"]["ui"]["marshmallow"] == {
        "base-classes": ["aaa.BlahUISchema"],
        "class": "test.services.records.ui_schema.TestUISchema",
        "extra-code": "",
        "generate": True,
        "imports": [{"alias": "aaa", "import": "aaa"}],
        "module": "test.services.records.ui_schema",
    }
    # assert that "a" is read & write false
    property_a = loaded_model["model"]["properties"]["metadata"]["properties"]["a"]
    assert property_a["marshmallow"]["read"] is False
    assert property_a["marshmallow"]["write"] is False
    assert property_a["ui"]["marshmallow"]["read"] is False
    assert property_a["ui"]["marshmallow"]["write"] is False

    schema = fs.read("test/services/records/schema.py")
    print(schema)
    assert "class TestSchema(BlahSchema)" in schema
    assert "class TestMetadataSchema(BlahMetadataSchema)" in schema
    assert "metadata = ma_fields.Nested(lambda: TestMetadataSchema())" in schema

    schema = fs.read("test/services/records/ui_schema.py")
    print(schema)
    assert "class TestUISchema(BlahUISchema)" in schema
    assert "class TestMetadataUISchema(BlahMetadataUISchema)" in schema
    assert "metadata = ma_fields.Nested(lambda: TestMetadataUISchema())" in schema


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
