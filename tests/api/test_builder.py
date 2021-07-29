from oarepo_model_builder.builders import JSONSchemaBuilder
from oarepo_model_builder.builders import MappingBuilder
from oarepo_model_builder.builders import DataModelBuilder
from oarepo_model_builder.proxies import current_model_builder


def test_datamodel_builder(app, datamodel_json):
    build = DataModelBuilder()
    el_handlers = [MappingBuilder(), JSONSchemaBuilder()]

    config = current_model_builder.model_config

    outputs = {}
    build(el=datamodel_json, config=config, path=[], outputs=outputs, handlers=el_handlers)

    assert len(outputs) == 2
    assert 'mapping' in outputs
    assert 'jsonschema' in outputs
