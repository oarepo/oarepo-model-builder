from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack


class TypeShortcutsPreprocessor(PropertyPreprocessor):
    TYPE = "type_shortcuts"

    @process(
        model_builder="*",
        path="/model/**",
        condition=lambda current, stack: stack.schema_valid,
    )
    def modify_type_shortcuts(self, data, stack: ModelBuilderStack, **kwargs):
        top = stack.top

        if not top.schema_element_type:
            return data

        self.set_type(top.schema_element_type, data)
        self.set_child_arrays(top.schema_element_type, data)

        return data

    def set_type(self, element_type, data):
        if not isinstance(data, dict):
            return

        if "type" in data:
            return

        if element_type in ("property", "items"):
            if (
                "properties" in data
                or "additionalProperties" in data
                or "unprocessedProperties" in data
            ):
                data["type"] = "object"
            elif "items" in data:
                data["type"] = "array"

    def set_child_arrays(self, element_type, data):
        if element_type == "properties":
            for k, v in list(data.items()):
                if k.endswith("[]"):
                    data.pop(k)
                    data[k[:-2]] = self.create_array(v)

    @staticmethod
    def create_array(value):
        ret = {}
        array = {}
        for k, v in value.items():
            if k.endswith("[]"):
                ret[k[:-2]] = v
            else:
                array[k] = v
        ret["type"] = "array"
        ret["items"] = array
        return ret

    @process(
        model_builder="*",
        path="/model",
        condition=lambda current, stack: stack.schema_valid,
    )
    def add_model_type(self, data, stack: ModelBuilderStack, **kwargs):
        if "type" not in data:
            data["type"] = "object"
        return data
