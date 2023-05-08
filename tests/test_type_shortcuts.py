import os

import json5

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema


def test_object():
    data = build_jsonschema(
        {"properties": {"a": {"properties": {"b": {"type": "keyword"}}}}}
    )

    assert data == {
        "type": "object",
        "properties": {
            "a": {"type": "object", "properties": {"b": {"type": "string"}}}
        },
    }


def test_array():
    data = build_jsonschema({"properties": {"a": {"items": {"type": "keyword"}}}})

    assert data == {
        "type": "object",
        "properties": {"a": {"type": "array", "items": {"type": "string"}}},
    }


def test_object_inside_array():
    data = build_jsonschema(
        {"properties": {"a": {"items": {"properties": {"b": {"type": "keyword"}}}}}}
    )

    assert data == {
        "type": "object",
        "properties": {
            "a": {
                "type": "array",
                "items": {"type": "object", "properties": {"b": {"type": "string"}}},
            }
        },
    }


def test_array_brackets():
    data = build_jsonschema(
        {"properties": {"a[]": {"type": "keyword", "^minItems": 5}}}
    )

    assert data == {
        "type": "object",
        "properties": {
            "a": {
                "type": "array",
                "items": {"type": "string"},
            }
        },
    }


def build_jsonschema(model):
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
                "record": {"module": {"qualified": "test"}, **model},
            },
        ),
        profile="record",
        model_path=["record"],
        output_dir="",
    )
    return json5.load(
        builder.filesystem.open(
            os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
        )
    )
