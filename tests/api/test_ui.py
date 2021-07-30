from oarepo_model_builder.builders import DataModelBuilder
from oarepo_model_builder.builders import UIBuilder
from oarepo_model_builder.proxies import current_model_builder


def test_ui_builder(datamodel_json):
    build = DataModelBuilder()
    el_handlers = [UIBuilder()]

    config = current_model_builder.model_config

    outputs = {}
    build(el=datamodel_json, config=config, path=[], outputs=outputs, handlers=el_handlers)

    assert len(outputs) == 1
    print(outputs['ui'].data)
