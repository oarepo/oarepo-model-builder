import yaml

from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
import munch


class TypeShortcutsPreprocessor(PropertyPreprocessor):
    TYPE = "type_shortcuts"

    @process(
        model_builder="*",
        path="**",
        condition=lambda current, stack: stack.schema_valid,
    )
    def modify_type_shortcuts(self, data, stack: ModelBuilderStack, **kwargs):
        top = stack.top

        if not top.schema_element_type:
            return data

        if top.schema_element_type == "property":
            data = self.expand_single_line_def(data)
            data = munch.munchify(data, factory=HyphenMunch)
            self.set_property_type(data)
        elif top.schema_element_type == "items":
            data = self.expand_single_line_def(data)
            data = munch.munchify(data, factory=HyphenMunch)
            self.set_property_type(data)

        if top.schema_element_type == "properties":
            self.expand_child_shortcuts(data)

        return data

    @staticmethod
    def expand_single_line_def(data):
        if not isinstance(data, str):
            return data
        if "{" not in data:
            return {"type": data}
        datatype, constraints = data.split("{", maxsplit=1)
        constraints = constraints.replace(":", ": ")
        return {"type": datatype, **yaml.safe_load("blah: {" + constraints)["blah"]}

    def set_property_type(self, data):
        if "type" in data:
            return

        if (
            "properties" in data
            or "additionalProperties" in data
            or "unprocessedProperties" in data
        ):
            data["type"] = "object"
        elif "items" in data:
            data["type"] = "array"

    def expand_child_shortcuts(self, data):
        for k, v in list(data.items()):
            if k.endswith("[]"):
                data.pop(k)
                data[k[:-2]] = self.create_array(v)
            if k.endswith("{}"):
                data.pop(k)
                data[k[:-2]] = self.create_object(v, datatype="object")
            if k.endswith("{nested}"):
                data.pop(k)
                data[k[:-8]] = self.create_object(v, datatype="nested")

    @staticmethod
    def create_array(value):
        array, array_item = TypeShortcutsPreprocessor.separate_properties(value)
        array["type"] = "array"
        array["items"] = array_item
        return array

    @staticmethod
    def create_object(value, datatype):
        obj, obj_items = TypeShortcutsPreprocessor.separate_properties(value)
        obj["type"] = datatype
        obj["properties"] = obj_items
        return obj

    @staticmethod
    def separate_properties(value):
        value = TypeShortcutsPreprocessor.expand_single_line_def(value)
        container = {}
        container_item = {}
        for k, v in value.items():
            if not k:
                continue
            if k[0] == "^":
                container[k[1:]] = v
            else:
                container_item[k] = v
        return munch.munchify(container, factory=HyphenMunch), munch.munchify(
            container_item, factory=HyphenMunch
        )

    @process(
        model_builder="*",
        path="/model",
        condition=lambda current, stack: stack.schema_valid,
    )
    def add_model_type(self, data, stack: ModelBuilderStack, **kwargs):
        if "type" not in data:
            data["type"] = "object"
        return data
