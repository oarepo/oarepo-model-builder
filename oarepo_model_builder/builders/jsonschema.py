from ..datatypes import Section
from ..utils.dict import dict_get
from .json_base import JSONBaseBuilder


class JSONSchemaBuilder(JSONBaseBuilder):
    TYPE = "jsonschema"
    output_file_type = "jsonschema"
    output_file_name = ["json-schema-settings", "file"]
    parent_module_root_name = "jsonschemas"
    create_parent_packages = True

    def build_node(self, node):
        skip = dict_get(
            self.current_model.definition, ["json-schema-settings", "skip"], False
        )
        if skip:
            return
        generated = self.generate(node)
        self.output.merge(generated)

    def generate(self, node):
        json_schema: Section = node.section_json_schema
        ret = {**json_schema.config}

        if json_schema.children:
            properties = ret.setdefault("properties", {})
            for k, v in json_schema.children.items():
                v = self.generate(v)
                properties[k] = v
        if json_schema.item:
            ret["items"] = self.generate(json_schema.item)
        return ret
