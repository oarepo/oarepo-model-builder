import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.model_preprocessors.default_values import (
    DefaultValuesModelPreprocessor,
)
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema
from tests.mock_filesystem import MockFilesystem
from tests.multilang import MultilangPreprocessor

try:
    import json5
except ImportError:
    import json as json5


def test_simple_mapping_builder():
    model = {"properties": {"a": {"type": "keyword", "mapping": {"type": "text"}}}}
    data = build_model(model)

    assert data == {"mappings": {"properties": {"a": {"type": "text"}}}}


def test_array_mapping_builder():
    model = {
        "properties": {
            "a": {
                "type": "array",
                "items": {"type": "keyword", "mapping": {"type": "text"}},
            }
        }
    }
    data = build_model(model)

    assert data == {"mappings": {"properties": {"a": {"type": "text"}}}}


def build_model(model):
    builder = ModelBuilder(
        output_builders=[MappingBuilder],
        outputs=[MappingOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        filesystem=MockFilesystem(),
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {"use_isort": False, "use_black": False},
                    "opensearch": {"version": "os-v2", "templates": {"os-v2": {}}},
                },
                "model": {"package": "test", **model},
            },
        ),
        output_dir="",
    )
    data = json5.load(
        builder.filesystem.open(
            os.path.join(
                "test", "records", "mappings", "os-v2", "test", "test-1.0.0.json"
            )
        )
    )
    return data


def test_mapping_preprocessor():
    builder = ModelBuilder(
        output_builders=[MappingBuilder],
        outputs=[MappingOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        property_preprocessors=[MultilangPreprocessor],
        included_validation_schemas=[
            {
                "jsonschema-property": {
                    "properties": {"type": {"enum": ["multilingual"]}}
                }
            }
        ],
        filesystem=MockFilesystem(),
    )

    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {"use_isort": False, "use_black": False},
                    "opensearch": {"version": "os-v2", "templates": {"os-v2": {}}},
                },
                "model": {
                    "package": "test",
                    "properties": {"a": {"type": "multilingual"}},
                },
            },
        ),
        output_dir="",
    )

    data = json5.load(
        builder.filesystem.open(
            os.path.join(
                "test", "records", "mappings", "os-v2", "test", "test-1.0.0.json"
            )
        )
    )

    assert data == {
        "mappings": {
            "properties": {
                "a": {
                    "type": "object",
                    "properties": {
                        "lang": {"type": "keyword"},
                        "value": {"type": "text"},
                    },
                },
                "a_cs": {"type": "text"},
            }
        }
    }
