from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.source import DataModelBuilder
from oarepo_model_builder.proxies import current_model_builder


def test_jsonschema_builder(app, datamodel_json):
    build = DataModelBuilder()
    el_handlers = [JSONSchemaBuilder()]

    config = current_model_builder.model_config

    outputs = {}
    build(el=datamodel_json, config=config, path=[], outputs=outputs, handlers=el_handlers)

    assert len(outputs) == 1
    print(outputs['jsonschema'].data)
