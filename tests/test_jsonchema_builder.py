import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders import OutputBuilderComponent
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.model_preprocessors.default_values import \
    DefaultValuesModelPreprocessor
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.validation.model_validation import model_validator
from tests.multilang import (MultilangPreprocessor, MultilingualDataType,
                             UIValidator)

try:
    import json5
except ImportError:
    import json as json5


def test_simple_jsonschema_builder():
    data = build({"properties": {"a": {"type": "keyword", "ui": {"class": "bolder"}}}})

    assert data == {"type": "object", "properties": {"a": {"type": "keyword"}}}


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
        "properties": {"a": {"type": "keyword"}},
        "required": ["a"],
    }


def test_required_inside_metadata():
    data = build(
        {
            "properties": {
                "metadata": {
                    "properties": {
                        "a": {
                            "type": "keyword",
                            "required": True,
                            "ui": {"class": "bolder"},
                        }
                    }
                }
            }
        }
    )

    assert data == {
        "type": "object",
        "properties": {
            "metadata": {
                "type": "object",
                "properties": {"a": {"type": "keyword"}},
                "required": ["a"],
            }
        },
    }


def test_min_length():
    data = build({"properties": {"a": {"type": "keyword", "minLength": 5}}})
    assert data == {
        "type": "object",
        "properties": {"a": {"type": "keyword", "minLength": 5}},
    }


def test_jsonschema_preprocessor():
    data = build(
        {"properties": {"a": {"type": "multilingual", "ui": {"class": "bolder"}}}},
        property_preprocessors=[MultilangPreprocessor],
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


class TestJSONSchemaOutputComponent(OutputBuilderComponent):
    def model_element_enter(self, builder, data, *, stack):
        if "type" in data:
            data["type"] = "integer"
        return data


def test_components():
    data = build(
        {"properties": {"a": {"type": "keyword", "ui": {"class": "bolder"}}}},
        output_builder_components={
            JSONSchemaOutput.TYPE: [TestJSONSchemaOutputComponent]
        },
    )

    assert data == {"type": "object", "properties": {"a": {"type": "integer"}}}


def build(model, output_builder_components=None, property_preprocessors=None):
    datatypes._prepare_datatypes()
    if UIValidator not in model_validator.validator_map["property"]:
        model_validator.validator_map["property"].append(UIValidator)
    datatypes.datatype_map["multilingual"] = MultilingualDataType
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        output_builder_components=output_builder_components,
        filesystem=InMemoryFileSystem(),
        property_preprocessors=property_preprocessors,
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {"use-isort": False, "use-black": False},
                },
                "model": {
                    "package": "test",
                    **model,
                },
            },
        ),
        output_dir="",
    )
    data = json5.load(
        builder.filesystem.open(
            os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
        )
    )
    return data
