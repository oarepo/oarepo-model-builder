from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.schema import ModelSchema


def test_empty_builder():
    builder = ModelBuilder(output_builders=[], outputs=[], property_preprocessors=[])
    outputs = builder.build(ModelSchema("", {"a": 1}), "/tmp/test")
    assert outputs == {}


def test_transformer():
    class SampleModelPreprocessor(ModelPreprocessor):
        def transform(self, schema, settings):
            schema.set("test", 1)

    builder = ModelBuilder(
        output_builders=[],
        outputs=[],
        property_preprocessors=[],
        model_preprocessors=[SampleModelPreprocessor],
    )
    schema = ModelSchema("", {"a": 2})
    builder.build(schema, "/tmp/test")

    assert schema.get("test") == 1
    assert schema.get("a") == 2
