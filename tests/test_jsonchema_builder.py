import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema
from tests.multilang import MultilingualDataType, UIDataTypeComponent

try:
    import json5
except ImportError:
    import json as json5


def test_simple_jsonschema_builder():
    data = build({"properties": {"a": {"type": "keyword", "ui": {"class": "bolder"}}}})

    assert data == {"type": "object", "properties": {"a": {"type": "string"}}}


def test_required():
    data = build(
        {
            "properties": {
                "a": {
                    "type": "keyword",
                    "required": True,
                    "ui": {"class": "bolder"},
                }
            }
        }
    )

    assert data == {
        "type": "object",
        "properties": {"a": {"type": "string"}},
    }


def test_required_inside_metadata():
    data = build(
        {
            "properties": {
                "metadata": {
                    "marshmallow": {},  # just for debugging
                    "properties": {
                        "a": {
                            "type": "keyword",
                            "required": True,
                            "ui": {"class": "bolder"},
                        }
                    },
                }
            },
        }
    )

    assert data == {
        "type": "object",
        "properties": {
            "metadata": {
                "type": "object",
                "properties": {"a": {"type": "string"}},
            }
        },
    }


def test_min_length():
    data = build({"properties": {"a": {"type": "keyword", "minLength": 5}}})
    assert data == {
        "type": "object",
        "properties": {"a": {"type": "string"}},
    }


def test_jsonschema_preprocessor():
    data = build(
        {"properties": {"a": {"type": "multilingual", "ui": {"class": "bolder"}}}},
    )

    assert data == {
        "type": "object",
        "properties": {
            "a": {
                "type": "object",
                "properties": {
                    "lang": {"type": "string"},
                    "value": {"type": "string"},
                },
            }
        },
    }


def build(model):
    datatypes.datatype_map["multilingual"] = MultilingualDataType

    # remove ui component as we are providing our own
    for ci, c in reversed(list(enumerate(datatypes.components))):
        if "UI" in type(c).__name__:
            del datatypes.components[ci]

    datatypes.components.append(UIDataTypeComponent())
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        filesystem=InMemoryFileSystem(),
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {
                        "use-isort": False,
                        "use-black": False,
                        "use-autoflake": False,
                    },
                },
                "record": {
                    "module": {"qualified": "test"},
                    **model,
                },
            },
        ),
        profile="record",
        model_path=["record"],
        output_dir="",
    )
    data = json5.load(
        builder.filesystem.open(
            os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
        )
    )
    return data
