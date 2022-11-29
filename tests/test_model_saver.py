import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.inherited_model import InheritedModelBuilder
from oarepo_model_builder.builders.model_saver import (
    ModelSaverBuilder,
    ModelRegistrationBuilder,
)
from oarepo_model_builder.model_preprocessors.default_values import (
    DefaultValuesModelPreprocessor,
)
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.outputs.json import JSONOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.inherited_model import (
    InheritedModelPreprocessor,
)
from oarepo_model_builder.property_preprocessors.marshmallow_class_generator import (
    MarshmallowClassGeneratorPreprocessor,
)
from oarepo_model_builder.property_preprocessors.marshmallow_validators_generator import (
    ValidatorsPreprocessor,
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
                "a": {"type": "keyword", "oarepo:ui": {"class": "bolder"}},
                "b": {
                    "type": "object",
                    "properties": {
                        "c": {
                            "type": "keyword",
                        }
                    },
                    "oarepo:marshmallow": {"generate": True},
                },
                "metadata": {"properties": {}},
            }
        },
        property_preprocessors=[
            MarshmallowClassGeneratorPreprocessor,
            ValidatorsPreprocessor,
            InheritedModelPreprocessor,
        ],
    )

    assert data[0] == {
        "settings": {
            "collection-url": "/test/",
            "index-name": "test-test-1.0.0",
            "jsonschemas-package": "test.records.jsonschemas",
            "kebap-package": "test",
            "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
            "mapping-package": "test.records.mappings",
            "model-name": "test",
            "package": "test",
            "package-base": "test",
            "package-base-upper": "TEST",
            "package-path": "test",
            "processing-order": ["settings", "*", "model"],
            "python": {"use_black": False, "use_isort": False, "record-prefix": "Test"},
            "saved-model-file": "test/models/model.json",
            "inherited-model-file": "test/models/inherited_model.json",
            "schema-file": "test/records/jsonschemas/test-1.0.0.json",
            "schema-name": "test-1.0.0.json",
            "schema-server": "http://localhost/schemas/",
            "schema-version": "1.0.0",
        },
        "model": {
            "properties": {
                "a": {"oarepo:ui": {"class": "bolder"}, "type": "keyword"},
                "b": {
                    "oarepo:marshmallow": {"generate": True},
                    "properties": {"c": {"type": "keyword"}},
                    "type": "object",
                },
                "metadata": {"properties": {}},
            }
        },
    }
    assert data[1] == {
        "model": {
            "oarepo:marshmallow": {
                "base-classes": ["test.services.schema.TestRecordSchema"],
                "generate": True,
            },
            "properties": {
                "a": {
                    "oarepo:marshmallow": {"read": False, "write": False},
                    "oarepo:ui": {"class": "bolder"},
                    "type": "keyword",
                },
                "b": {
                    "oarepo:marshmallow": {
                        "generate": True,
                        "read": False,
                        "write": False,
                    },
                    "properties": {
                        "c": {
                            "oarepo:marshmallow": {"read": False, "write": False},
                            "type": "keyword",
                        }
                    },
                    "type": "object",
                },
                "metadata": {
                    "oarepo:marshmallow": {
                        "base-classes": ["test.services.schema.TestMetadataSchema"],
                        "generate": True,
                    },
                    "properties": {},
                },
            },
        },
        "settings": {"python": {}},
    }
    assert data[2].strip() == ""
    assert (
        data[3].strip()
        == """[options.entry_points]
oarepo.models = test = test.models:model.json"""
    )


def build(model, output_builder_components=None, property_preprocessors=None):
    builder = ModelBuilder(
        output_builders=[
            ModelSaverBuilder,
            ModelRegistrationBuilder,
            InheritedModelBuilder,
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
        json5.load(
            builder.filesystem.open(
                os.path.join("test", "models", "inherited_model.json")
            )
        ),
        builder.filesystem.read(os.path.join("test", "models", "__init__.py")),
        builder.filesystem.read("setup.cfg"),
    )
