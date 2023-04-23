from pathlib import Path

from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class JSONSchemaBuilder(JSONBaseBuilder):
    TYPE = "jsonschema"
    output_file_type = "jsonschema"
    output_file_name = "schema-file"
    parent_module_root_name = "jsonschemas"

    def build_node(self, node):
        self.output.merge(node.json_schema)
