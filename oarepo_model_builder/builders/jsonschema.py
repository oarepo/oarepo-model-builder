from pathlib import Path

from . import process
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class JSONSchemaBuilder(JSONBaseBuilder):
    TYPE = "jsonschema"
    output_file_type = "jsonschema"
    output_file_name = "schema-file"
    parent_module_root_name = "jsonschemas"

    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def model_element(self):
        if self.stack.top.schema_element_type is None and self.stack.top.key == "required":
            return
        self.model_element_enter()
        self.build_children()
        if self.stack.top.schema_element_type == "items" or self.stack.top.schema_element_type == "property":
            self.check_and_output_required()
        self.model_element_leave()

    def check_and_output_required(self):
        top_data = self.stack.top.data
        if isinstance(top_data, dict) and "properties" in top_data:
            required = []
            for k, v in top_data["properties"].items():
                if isinstance(v, dict) and v.get("required", False):
                    required.append(k)
            if required:
                required.sort()
                self.output.primitive("required", required)

    def on_enter_model(self, output_name):
        ensure_parent_modules(self.builder, Path(output_name), ends_at=self.parent_module_root_name)

    def on_leave_model(self):
        self.check_and_output_required()
