from oarepo_model_builder.builders.extend import ExtendBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack


class DisableMarshmallowPreprocessor(PropertyPreprocessor):
    TYPE = "disable-marshmallow"

    @process(
        model_builder=ExtendBuilder,
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type == "property",
    )
    def modify_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        marshmallow_def = "marshmallow"
        if marshmallow_def not in data:
            data["marshmallow"] = {"read": False, "write": False}
            return data
        marshmallow = data[marshmallow_def]
        if "schema-class" in marshmallow:
            # already generated - if user wants to override this, he has to set schema-class and generate
            marshmallow["generate"] = False
            schema_class = marshmallow.pop("schema-class")
            if not marshmallow.get("field", None):
                marshmallow["inherited-schema-class"] = schema_class

        marshmallow["read"] = False
        marshmallow["write"] = False

        return data
