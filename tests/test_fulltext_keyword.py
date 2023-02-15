import os

import json5
import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.model_preprocessors.default_values import \
    DefaultValuesModelPreprocessor
from oarepo_model_builder.model_preprocessors.opensearch import \
    OpensearchModelPreprocessor
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.datatype_preprocessor import \
    DataTypePreprocessor
from oarepo_model_builder.schema import ModelSchema


def get_model_schema(field_type):
    return ModelSchema(
        "",
        {
            "settings": {
                "python": {"use-isort": False, "use-black": False},
            },
            "model": {"package": "test", "properties": {"a": {"type": field_type}}},
        },
    )


@pytest.fixture
def fulltext_builder():
    return ModelBuilder(
        output_builders=[JSONSchemaBuilder, MappingBuilder],
        outputs=[JSONSchemaOutput, MappingOutput, PythonOutput],
        model_preprocessors=[
            DefaultValuesModelPreprocessor,
            OpensearchModelPreprocessor,
        ],
        property_preprocessors=[DataTypePreprocessor],
    )


def test_fulltext(fulltext_builder):
    schema = get_model_schema("fulltext")
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    data = load_generated_jsonschema(fulltext_builder)

    assert data == {"type": "object", "properties": {"a": {"type": "string"}}}

    data = load_generated_mapping(fulltext_builder)

    assert data == {
        "mappings": {
            "properties": {
                "a": {"type": "text"},
            }
        }
    }


def test_keyword(fulltext_builder):
    schema = get_model_schema("keyword")
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    data = load_generated_jsonschema(fulltext_builder)

    assert data == {"type": "object", "properties": {"a": {"type": "string"}}}

    data = load_generated_mapping(fulltext_builder)

    assert data == {
        "mappings": {
            "properties": {
                "a": {"type": "keyword"},
            }
        }
    }


def test_fulltext_keyword(fulltext_builder):
    schema = get_model_schema("fulltext+keyword")
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    data = load_generated_jsonschema(fulltext_builder)

    assert data == {"type": "object", "properties": {"a": {"type": "string"}}}

    data = load_generated_mapping(fulltext_builder)

    assert data == {
        "mappings": {
            "properties": {
                "a": {
                    "fields": {"keyword": {"type": "keyword"}},
                    "type": "text",
                },
            }
        }
    }


def load_generated_mapping(fulltext_builder):
    return json5.load(
        fulltext_builder.filesystem.open(
            os.path.join(
                "test", "records", "mappings", "os-v2", "test", "test-1.0.0.json"
            )
        )
    )


def load_generated_jsonschema(fulltext_builder):
    return json5.load(
        fulltext_builder.filesystem.open(
            os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
        )
    )
