from oarepo_model_builder.builders import JSONSchemaBuilder
from oarepo_model_builder.builders import MappingBuilder
from oarepo_model_builder.builders import DataModelBuilder
from oarepo_model_builder.proxies import current_model_builder


def test_datamodel_builder(datamodel_json, model_config):
    build = DataModelBuilder()
    el_handlers = [MappingBuilder(), JSONSchemaBuilder()]

    outputs = {}
    build(el=datamodel_json, config=model_config, path=[], outputs=outputs, handlers=el_handlers)

    assert len(outputs) == 2
    assert 'mapping' in outputs
    assert 'jsonschema' in outputs
