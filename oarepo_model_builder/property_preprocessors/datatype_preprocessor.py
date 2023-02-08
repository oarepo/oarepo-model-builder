from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.invenio.invenio_record_schema import \
    InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import (PropertyPreprocessor,
                                                         process)
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge


class DataTypePreprocessor(PropertyPreprocessor):
    TYPE = "datatype"

    @process(
        model_builder=JSONSchemaBuilder,
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type
        in ("property", "items"),
    )
    def modify_jsonschema(self, data, stack: ModelBuilderStack, **kwargs):
        datatype = datatypes.get_datatype(
            data, stack.top.key, self.schema.current_model, self.schema, stack
        )
        if not datatype:
            return data
        self.merge_with_data(data, datatype.model_schema())
        return datatype.json_schema()

    @process(
        model_builder=MappingBuilder,
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type
        in ("property", "items"),
    )
    def modify_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        datatype = datatypes.get_datatype(
            data, stack.top.key, self.schema.current_model, self.schema, stack
        )
        if not datatype:
            return data
        self.merge_with_data(data, datatype.model_schema())
        return datatype.mapping()

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type
        in ("property", "items"),
    )
    def modify_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        datatype = datatypes.get_datatype(
            data, stack.top.key, self.schema.current_model, self.schema, stack
        )
        if not datatype:
            return data
        self.merge_with_data(data, datatype.model_schema())
        ret = datatype.marshmallow()
        imports = datatype.imports()
        ret.setdefault("imports", []).extend(
            [
                {"import": i.import_path, "alias": i.alias}
                if i.alias
                else {"import": i.import_path}
                for i in imports
            ]
        )

    @process(
        model_builder="*",
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type
        in ("property", "items"),
        priority=-100,  # fallback priority
    )
    def modify_generic(
        self, data, stack: ModelBuilderStack, output_builder_type, **kwargs
    ):
        datatype = datatypes.get_datatype(
            data, stack.top.key, self.schema.current_model, self.schema, stack
        )
        if not datatype:
            return data
        self.merge_with_data(data, datatype.model_schema())
        method = getattr(datatype, "process_" + output_builder_type, None)
        if method and callable(method):
            return method()
        return data

    def merge_with_data(self, data, extra_schema):
        if extra_schema:
            return deepmerge(data, extra_schema)
        return data
