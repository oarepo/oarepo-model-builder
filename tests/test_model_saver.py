import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.model_saver import ModelSaverBuilder, ModelRegistrationBuilder
from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.outputs.json import JSONOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema
from tests.mock_filesystem import MockFilesystem

try:
    import json5
except ImportError:
    import json as json5


def test_model_saver():
    data = build({"properties": {"a": {"type": "keyword", "oarepo:ui": {"class": "bolder"}}}})

    assert data[0] == {
        'settings': {
            'collection-url': '/test/',
            'index-name': 'test-test-1.0.0',
            'jsonschemas-package': 'test.records.jsonschemas',
            'kebap-package': 'test',
            'mapping-file': 'test/records/mappings/v7/test/test-1.0.0.json',
            'mapping-package': 'test.records.mappings',
            'model-name': 'test',
            'package': 'test',
            'package-base': 'test',
            'package-base-upper': 'TEST',
            'package-path': 'test',
            'processing-order': ['settings', '*', 'model'],
            'python': {'use_black': False, 'use_isort': False},
            'saved-model-file': 'models/model.json',
            'schema-file': 'test/records/jsonschemas/test-1.0.0.json',
            'schema-name': 'test-1.0.0.json',
            'schema-server': 'http://localhost/schemas/',
            'schema-version': '1.0.0'
        },
        "model": {
            "properties": {
                "a": {
                    "type": "keyword",
                    "oarepo:ui": {
                        "class": "bolder"
                    }
                }
            }
        }
    }
    assert data[1].strip() == ""
    assert data[2].strip() == """[options.entry_points]
oarepo.models = test = test.models:model.json"""


def build(model, output_builder_components=None, property_preprocessors=None):
    builder = ModelBuilder(
        output_builders=[ModelSaverBuilder, ModelRegistrationBuilder],
        outputs=[JSONOutput, PythonOutput, CFGOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        output_builder_components=output_builder_components,
        filesystem=MockFilesystem(),
        property_preprocessors=property_preprocessors,
        included_validation_schemas=[
            {
                "jsonschema-property": {
                    "properties": {
                        "type": {"enum": ["multilingual"]},
                        "oarepo:ui": {"type": "object", "additionalProperties": True},
                    }
                }
            }
        ],
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
    json5.load(builder.filesystem.open(os.path.join("models", "model.json")))
    return (
        json5.load(builder.filesystem.open(os.path.join("models", "model.json"))),
        builder.filesystem.read(os.path.join("models", "__init__.py")),
        builder.filesystem.read("setup.cfg")
    )
