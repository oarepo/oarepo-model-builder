from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.transformers import ModelTransformer


def test_empty_builder():
    builder = ModelBuilder(
        output_builders=[],
        outputs=[],
        output_preprocessors=[]
    )
    outputs = builder.build(ModelSchema('', {'a': 1}), '/tmp/test')
    assert outputs == {}


def test_transformer():
    class SampleTransformer(ModelTransformer):
        def transform(self, schema):
            schema.set('test', 1)

    builder = ModelBuilder(
        output_builders=[],
        outputs=[],
        output_preprocessors=[],
        transformers=[SampleTransformer]
    )
    schema = ModelSchema('', {'a': 2})
    builder.build(schema, '/tmp/test')

    assert schema.get('test') == 1
    assert schema.get('a') == 2

