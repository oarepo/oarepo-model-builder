import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.model_saver import (
    ModelRegistrationBuilder,
    ModelSaverBuilder,
)
from oarepo_model_builder.model_preprocessors.default_values import (
    DefaultValuesModelPreprocessor,
)
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.outputs.json import JSONOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.datatype_preprocessor import (
    DataTypePreprocessor,
)
from oarepo_model_builder.schema import ModelSchema
from tests.mock_filesystem import MockFilesystem

try:
    import json5
except ImportError:
    import json as json5


def test_model_saver():
    data = build(
        {
            "properties": {
                "a": {"type": "keyword", "ui": {"class": "bolder"}},
                "b": {
                    "type": "object",
                    "properties": {
                        "c": {
                            "type": "keyword",
                        }
                    },
                    "marshmallow": {"generate": True},
                },
                "metadata": {"properties": {}},
            }
        },
        property_preprocessors=[
            DataTypePreprocessor,
        ],
    )

    assert data[0] == {
        "type": "object",
        "properties": {
            "a": {"ui": {"class": "bolder"}, "type": "keyword"},
            "b": {
                "marshmallow": {"generate": True},
                "properties": {"c": {"type": "keyword"}},
                "type": "object",
            },
            "metadata": {"properties": {}},
        },
    }

    assert data[1].strip() == ""
    assert (
        data[2].strip()
        == """[options.entry_points]
oarepo.models = test = test.models:model.json"""
    )


def build(model, output_builder_components=None, property_preprocessors=None):
    builder = ModelBuilder(
        output_builders=[
            ModelSaverBuilder,
            ModelRegistrationBuilder,
        ],
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
                        "ui": {"type": "object", "additionalProperties": True},
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
                    "python": {
                        "use_isort": False,
                        "use_black": False,
                        "record-prefix": "Test",
                    },
                },
                "model": model,
            },
        ),
        output_dir="",
    )
    return (
        json5.load(
            builder.filesystem.open(os.path.join("test", "models", "model.json"))
        ),
        builder.filesystem.read(os.path.join("test", "models", "__init__.py")),
        builder.filesystem.read("setup.cfg"),
    )
