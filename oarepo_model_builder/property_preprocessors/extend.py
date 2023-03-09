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
        self._process_marshmallow_def(data.setdefault("marshmallow", {}))
        self._process_marshmallow_def(
            data.setdefault("ui", {}).setdefault("marshmallow", {})
        )

    def _process_marshmallow_def(self, marshmallow):
        if not marshmallow:
            marshmallow.update({"read": False, "write": False})
        elif "schema-class" in marshmallow:
            # already generated - if user wants to override this, he has to set schema-class and generate
            marshmallow["generate"] = False
