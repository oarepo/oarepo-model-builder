from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack


class RawPreprocessor(PropertyPreprocessor):
    TYPE = "raw"

    @process(
        model_builder=JSONSchemaBuilder,
        path="**/properties/*",
        condition=lambda current, stack: current.type == "raw",
    )
    def modify_fulltext_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data.pop("type")
        return data

    @process(
        model_builder=MappingBuilder,
        path="**/properties/*",
        condition=lambda current, stack: current.type == "raw",
    )
    def modify_fulltext_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "flatten"
        return data

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties/*",
        condition=lambda current, stack: current.type == "raw",
    )
    def modify_fulltext_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "raw"
        return data
