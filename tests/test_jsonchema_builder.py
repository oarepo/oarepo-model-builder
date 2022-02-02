import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders import OutputBuilderComponent
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema
from tests.mock_filesystem import MockFilesystem
from tests.multilang import MultilangPreprocessor

try:
    import json5
except ImportError:
    import json as json5


def test_simple_jsonschema_builder():
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        filesystem=MockFilesystem(),
    )
    builder.build(
        schema=ModelSchema(
            "",
            {
                "settings": {
                    "package": "test",
                    "python": {"use_isort": False, "use_black": False},
                },
                "model": {"properties": {"a": {"type": "string", "oarepo:ui": {"class": "bolder"}}}},
            },
        ),
        output_dir="",
    )

    data = json5.load(builder.filesystem.open(os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")))

    assert data == {"properties": {"a": {"type": "string"}}}


def test_jsonschema_preprocessor():
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        property_preprocessors=[MultilangPreprocessor],
        filesystem=MockFilesystem(),
    )

    builder.build(
        schema=ModelSchema(
            "",
            {
                "settings": {
                    "package": "test",
                    "python": {"use_isort": False, "use_black": False},
                },
                "model": {"properties": {"a": {"type": "multilingual", "oarepo:ui": {"class": "bolder"}}}},
            },
        ),
        output_dir="",
    )

    data = json5.load(builder.filesystem.open(os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")))

    assert data == {
        "properties": {
            "a": {
                "type": "object",
                "properties": {"lang": {"type": "string"}, "value": {"type": "string"}},
            }
        }
    }


class TestJSONSchemaOutputComponent(OutputBuilderComponent):
    def model_element_enter(self, builder, data, *, stack):
        if "type" in data:
            data["type"] = "integer"
        return data


def test_components():
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        output_builder_components={JSONSchemaOutput.TYPE: [TestJSONSchemaOutputComponent]},
        filesystem=MockFilesystem(),
    )
    builder.build(
        schema=ModelSchema(
            "",
            {
                "settings": {
                    "package": "test",
                    "python": {"use_isort": False, "use_black": False},
                },
                "model": {"properties": {"a": {"type": "string", "oarepo:ui": {"class": "bolder"}}}},
            },
        ),
        output_dir="",
    )

    data = json5.load(builder.filesystem.open(os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")))

    assert data == {"properties": {"a": {"type": "integer"}}}
