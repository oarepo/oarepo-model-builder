import marshmallow as ma

from oarepo_model_builder.datatypes import DataType, DataTypeComponent, Section
from oarepo_model_builder.utils.deepmerge import deepmerge


class MultilangPreprocessor:
    # @process(
    #     model_builder=JSONSchemaBuilder,
    #     path="/properties/*",
    #     condition=lambda current, stack: current.type == "multilingual",
    # )
    def modify_multilang_schema(self, data, **__kwargs):
        data["type"] = "object"
        data["properties"] = {"lang": {"type": "string"}, "value": {"type": "string"}}
        return data

    # @process(
    #     model_builder=MappingBuilder,
    #     path="/properties/*",
    #     condition=lambda current, stack: current.type == "multilingual",
    # )
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

    # @process(
    #     model_builder=InvenioRecordSchemaBuilder,
    #     path="/properties/*",
    #     condition=lambda current, stack: current.type == "multilingual",
    # )
    def modify_multilang_marshmallow(self, data, **__kwargs):
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


class UIDataTypeComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(UIValidator)


class MultilingualDataType(DataType):
    model_type = "multilingual"

    @property
    def section_json_schema(self):
        return Section(
            "json_schema",
            config={
                "properties": {"lang": {"type": "string"}, "value": {"type": "string"}},
                "type": "object",
            },
            children={},
            item=None,
        )
