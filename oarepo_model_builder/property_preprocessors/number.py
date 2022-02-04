from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge


class NumberPreprocessor(PropertyPreprocessor):
    TYPE = "number"

    @process(
        model_builder=MappingBuilder,
        path="**/properties/*",
        condition=lambda current, stack: current.type == "number",
    )
    def modify_date_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "double"
        return data

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties/*",
        condition=lambda current, stack: current.type == "number",
    )
    def modify_date_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        deepmerge(data.setdefault("oarepo:marshmallow", {}), {"class": "ma_fields.Float"})
        return data
