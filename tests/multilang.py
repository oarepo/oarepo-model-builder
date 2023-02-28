import marshmallow as ma

from oarepo_model_builder.builders import ReplaceElement
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.utils.deepmerge import deepmerge


class MultilangPreprocessor(PropertyPreprocessor):
    @process(
        model_builder=JSONSchemaBuilder,
        path="/properties/*",
        condition=lambda current, stack: current.type == "multilingual",
    )
    def modify_multilang_schema(self, data, stack, **kwargs):
        data["type"] = "object"
        data["properties"] = {"lang": {"type": "string"}, "value": {"type": "string"}}
        return data

    @process(
        model_builder=MappingBuilder,
        path="/properties/*",
        condition=lambda current, stack: current.type == "multilingual",
    )
    def modify_multilang_mapping(self, data, stack, **kwargs):
        raise ReplaceElement(
            {
                stack.top.key: {
                    "type": "object",
                    "properties": {
                        "lang": {"type": "keyword"},
                        "value": {"type": "text"},
                    },
                },
                stack.top.key + "_cs": {"type": "text"},
            }
        )

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="/properties/*",
        condition=lambda current, stack: current.type == "multilingual",
    )
    def modify_multilang_marshmallow(self, data, stack, **kwargs):
        data["type"] = "object"
        deepmerge(
            data.setdefault("marshmallow", {}),
            {
                "imports": [{"import": "tests.multilang", "alias": "multilingual"}],
                "class": "multilingual.MultilingualSchema",
                "nested": True,
            },
        )
        return data


class UIValidator(ma.Schema):
    class Meta:
        unknown = ma.INCLUDE


class MultilingualDataType(DataType):
    model_type = "multilingual"
    schema_type = "object"
    mapping_type = "object"
