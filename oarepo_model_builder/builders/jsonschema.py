from pathlib import Path

from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules
from ..datatypes import Section


class JSONSchemaBuilder(JSONBaseBuilder):
    TYPE = "jsonschema"
    output_file_type = "jsonschema"
    output_file_name = "schema-file"
    parent_module_root_name = "jsonschemas"

    def build_node(self, node):
        generated = self.generate(node)
        self.output.merge(generated)

    def generate(self, node):
        json_schema: Section = node.section_json_schema
        ret = {**json_schema.section}

        if json_schema.children:
            properties = ret.setdefault("properties", {})
            for k, v in json_schema.children.items():
                v = self.generate(v)
                properties[k] = v
        if json_schema.item:
            ret["items"] = self.generate(json_schema.item)
        return ret
