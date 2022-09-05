from oarepo_model_builder.builders.inherited_model_saver import InheritedModelSaverBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.camelcase import camel_case


class MarshmallowClassGeneratorPreprocessor(PropertyPreprocessor):
    TYPE = "marshmallow_class_generator"

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties",
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

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="/model$",
        condition=lambda current, stack: stack.schema_valid,
    )
    def modify_object_marshmallow_model(self, data, stack: ModelBuilderStack, **kwargs):
        self.add_root_class_name(stack)
        return data

    @process(
        model_builder=InheritedModelSaverBuilder,
        path="**/properties",
        condition=lambda current, stack: stack.schema_valid,
    )
    def modify_object_marshmallow_for_inherited(self, data, stack: ModelBuilderStack, **kwargs):
        schema_element_type = stack.top.schema_element_type
        # TODO: if top-level, add to base classes, else add 'generate: False'
        if schema_element_type == "properties":
            for k, v in stack.top.data.items():
                definition = self.add_class_name(stack, k, v)
                if definition:
                    definition['generate'] = False
        elif schema_element_type == "items":
            definition = self.add_class_name(stack, None, stack.top.data)
            if definition:
                definition['generate'] = False
        return data

    @process(
        model_builder=InheritedModelSaverBuilder,
        path="/model$",
        condition=lambda current, stack: stack.schema_valid,
    )
    def modify_object_marshmallow_model_for_inherited(self, data, stack: ModelBuilderStack, **kwargs):
        definition = self.add_root_class_name(stack)
        definition["base-classes"] = [definition.pop('class')]
        return data

    def add_class_name(self, stack, key, data):
        if "items" not in data and "properties" not in data:
            return
        definition = data.setdefault("oarepo:marshmallow", {})
        if "class" in definition:
            return
        definition["generate"] = True
        definition["class"] = f'{self.settings.package}.services.schema.' + \
                              camel_case(key or self.get_property_name(stack)) + "Schema"
        return definition

    def add_root_class_name(self, stack):
        data = stack.top.data
        definition = data.setdefault("oarepo:marshmallow", {})
        if "class" in definition:
            return definition
        definition["generate"] = True
        definition["class"] = f'{self.settings.package}.services.schema.RecordSchema'
        return definition

    def get_property_name(self, stack):
        for el in reversed(stack.stack):
            if el.schema_element_type == "property":
                return el.key
        return "UnknownName"
