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
        datatype = datatypes.get_datatype(data, stack.top.key, self.schema.current_model)
        if not datatype:
            return data
        return datatype.json_schema()

    @process(
        model_builder=MappingBuilder,
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type
        in ("property", "items"),
    )
    def modify_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        datatype = datatypes.get_datatype(data, stack.top.key, self.schema.current_model)
        if not datatype:
            return data
        return datatype.mapping()

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type
        in ("property", "items"),
    )
    def modify_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        datatype = datatypes.get_datatype(data, stack.top.key, self.schema.current_model)
        if not datatype:
            return data
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
