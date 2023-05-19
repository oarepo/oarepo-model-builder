from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.schema import ModelSchema


def test_empty_builder():
    builder = ModelBuilder(output_builders=[], outputs=[])
    builder.skip_schema_validation = True
    outputs = builder.build(
        ModelSchema("", {"a": 1}, validate=False), "record", ["record"], "/tmp/test"
    )
    assert outputs == {}
