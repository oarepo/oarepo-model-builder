from oarepo_model_builder.builders import JSONSchemaBuilder
from oarepo_model_builder.builders import DataModelBuilder
from oarepo_model_builder.proxies import current_model_builder


def test_jsonschema_builder(app, datamodel_json, model_config):
    build = DataModelBuilder()
    el_handlers = [JSONSchemaBuilder()]

    outputs = {}
    build(el=datamodel_json, config=model_config, path=[], outputs=outputs, handlers=el_handlers)

    assert len(outputs) == 1
    print(outputs['jsonschema'].data)
    assert outputs['jsonschema'].path.split('/')[-3:] == [
        'jsonschemas',
        'oarepo_model_builder',
        'oarepo-model-builder-1.0.0.json'
    ]