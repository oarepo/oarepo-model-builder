from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.schema import ModelSchema


def test_output_disabled():
    builder = ModelBuilder()
    schema = ModelSchema("", {"model": {"plugins": {"output": {"disable": "__all__"}}}})
    builder.set_schema(schema)
    assert builder._filter_classes([JSONSchemaOutput, MappingOutput], "output") == []


def test_output_disabled_single():
    builder = ModelBuilder()
    schema = ModelSchema(
        "", {"model": {"plugins": {"output": {"disable": ["jsonschema"]}}}}
    )
    builder.set_schema(schema)
    assert set(
        x.TYPE
        for x in builder._filter_classes([JSONSchemaOutput, MappingOutput], "output")
    ) == {"mapping"}


def test_output_enabled():
    builder = ModelBuilder()
    schema = ModelSchema(
        "",
        {
            "model": {
                "plugins": {"output": {"disable": "__all__", "enable": ["mapping"]}}
            }
        },
    )
    builder.set_schema(schema)
    assert set(
        x.TYPE
        for x in builder._filter_classes([JSONSchemaOutput, MappingOutput], "output")
    ) == {"mapping"}


def test_output_enabled_import():
    builder = ModelBuilder()
    schema = ModelSchema(
        "",
        {
            "model": {
                "plugins": {
                    "output": {
                        "include": [
                            "oarepo_model_builder.outputs.mapping:MappingOutput"
                        ]
                    }
                }
            }
        },
    )
    builder.set_schema(schema)
    assert set(x.TYPE for x in builder._filter_classes([], "output")) == {"mapping"}
