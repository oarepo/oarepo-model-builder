from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.invenio.invenio_script_sample_data import (
    InvenioScriptSampleDataBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge


class EnumPreprocessor(PropertyPreprocessor):
    TYPE = "enum"

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties/*",
        condition=lambda current, stack: stack.top.schema_element_type == "property",
    )
    def modify_date_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        if "enum" not in data:
            return data

        # TODO: support other datatypes than string
        alternatives = [f'"{x}"' for x in data["enum"]]

        deepmerge(
            data.setdefault("oarepo:marshmallow", {}),
            {"validators": [f'ma_valid.OneOf([{", ".join(alternatives)}])']},
        )
        return data

    @process(
        model_builder=JSONSchemaBuilder,
        path="**/properties/*",
        condition=lambda current, stack: stack.top.schema_element_type == "property",
    )
    def modify_date_jsonschema(self, data, stack: ModelBuilderStack, **kwargs):
        if "enum" not in data:
            return data

        deepmerge(data.setdefault("oarepo:jsonschema", {}), {"enum": data["enum"]})
        return data

    @process(
        model_builder=InvenioScriptSampleDataBuilder,
        path="**/properties/*",
        condition=lambda current, stack: stack.top.schema_element_type == "property",
    )
    def modify_date_sampledata(self, data, stack: ModelBuilderStack, **kwargs):
        if "enum" not in data:
            return data
        if "oarepo:sample" in data:
            return data
        data["oarepo:sample"] = data["enum"]
        return data
