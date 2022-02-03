import os

import json5

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.type_shortcuts import TypeShortcutsPreprocessor
from oarepo_model_builder.schema import ModelSchema
from tests.mock_filesystem import MockFilesystem


def test_object():
    data = build_jsonschema({"properties": {"a": {"properties": {"b": {"type": "string"}}}}})

    assert data == {
        "type": "object",
        "properties": {"a": {"type": "object", "properties": {"b": {"type": "string"}}}},
    }


def test_array():
    data = build_jsonschema({"properties": {"a": {"items": {"type": "string"}}}})

    assert data == {
        "type": "object",
        "properties": {"a": {"type": "array", "items": {"type": "string"}}},
    }


def test_object_inside_array():
    data = build_jsonschema({"properties": {"a": {"items": {"properties": {"b": {"type": "string"}}}}}})

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
    data = build_jsonschema({"properties": {"a[]": {"type": "string", "minLength[]": "just-for-test"}}})

    assert data == {
        "type": "object",
        "properties": {
            "a": {
                "type": "array",
                "minLength": "just-for-test",
                "items": {"type": "string"},
            }
        },
    }


def build_jsonschema(model):
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        property_preprocessors=[TypeShortcutsPreprocessor],
        filesystem=MockFilesystem(),
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "package": "test",
                    "python": {"use_isort": False, "use_black": False},
                },
                "model": model,
            },
        ),
        output_dir="",
    )
    return json5.load(builder.filesystem.open(os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")))
