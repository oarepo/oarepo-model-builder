from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge


class TextKeywordPreprocessor(PropertyPreprocessor):
    TYPE = "text_keyword"

    #
    # type='fulltext' in model
    #

    @process(
        model_builder=JSONSchemaBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "fulltext",
    )
    def modify_fulltext_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "string"
        return data

    @process(
        model_builder=MappingBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "fulltext",
    )
    def modify_fulltext_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "text"
        return data

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "fulltext",
    )
    def modify_fulltext_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "string"
        return data

    #
    # type='keyword' in model
    #

    @process(
        model_builder=JSONSchemaBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "keyword",
    )
    def modify_keyword_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "string"
        return data

    @process(
        model_builder=MappingBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "keyword",
    )
    def modify_keyword_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "keyword"
        extra = {}
        ignore_above = self.settings["opensearch"].get("keyword-ignore-above")
        if ignore_above:
            extra["ignore_above"] = ignore_above
        deepmerge(
            data.setdefault("oarepo:mapping", {}),
            extra,
        )
        return data

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "keyword",
    )
    def modify_keyword_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "string"
        return data

    #
    # type='fulltext+keyword' in model
    #

    @process(
        model_builder=JSONSchemaBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "fulltext+keyword",
    )
    def modify_fulltext_keyword_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "string"
        return data

    @process(
        model_builder=MappingBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "fulltext+keyword",
    )
    def modify_fulltext_keyword_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "text"
        ignore_above = self.settings["opensearch"].get("keyword-ignore-above")
        fld = {
            "type": "keyword",
        }
        if ignore_above:
            fld["ignore_above"] = ignore_above
        deepmerge(
            data.setdefault("oarepo:mapping", {}),
            {"fields": {"keyword": fld}},
            [],
        )
        return data

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path=("**/properties/*", "**/items"),
        condition=lambda current, stack: current.type == "fulltext+keyword",
    )
    def modify_fulltext_keyword_marshmallow(
        self, data, stack: ModelBuilderStack, **kwargs
    ):
        data["type"] = "string"
        return data

    def _call_method(self, data, stack: ModelBuilderStack, output_builder_type):
        for method, _output_builder_type in self.json_paths.match(
            stack.path, stack.top.data, extra_data={"stack": stack}
        ):
            if (
                _output_builder_type == "*"
                or output_builder_type == _output_builder_type
            ):
                return method(data, stack=stack)
