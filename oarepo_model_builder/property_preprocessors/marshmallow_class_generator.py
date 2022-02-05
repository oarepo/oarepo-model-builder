from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.camelcase import camel_case


class MarshmallowClassGeneratorPreprocessor(PropertyPreprocessor):
    TYPE = "marshmallow_class_generator"

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties/*",
        condition=lambda current, stack: stack.schema_valid,
    )
    def modify_object_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        schema_element_type = stack.top.schema_element_type

        if schema_element_type == "properties":
            for k, v in stack.top.data.items():
                self.add_class_name(stack, k, v)
        elif schema_element_type == "items":
            self.add_class_name(stack, None, stack.top.data)
        return data

    def add_class_name(self, stack, key, data):
        if "items" not in data and "properties" not in data:
            return
        definition = data.setdefault("oarepo:marshmallow", {})
        if "class" in definition:
            return
        definition["class"] = camel_case(key or self.get_property_name(stack)) + "Schema"

    def get_property_name(self, stack):
        for el in reversed(stack.stack):
            if el.schema_element_type == "property":
                return el.key
        return "UnknownName"
