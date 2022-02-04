from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.schema import Ref, is_schema_element, match_schema


class MarshmallowClassGeneratorPreprocessor(PropertyPreprocessor):
    TYPE = "marshmallow_class_generator"

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties/*",
        condition=lambda current, stack: is_schema_element(stack),
    )
    def modify_object_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        schema_path = match_schema(stack)
        if isinstance(schema_path[-1], Ref):
            schema_element_type = schema_path[-1].element_type
        else:
            schema_element_type = None

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
        definition["class"] = (key or self.get_property_name(stack)).title()

    def get_property_name(self, stack):
        schema_path = match_schema(stack)
        for idx, el in reversed(list(enumerate(schema_path))):
            el = schema_path.pop()

            if isinstance(el, Ref) and el.element_type == "property":
                return stack[idx].key

        return "UnknownName"
