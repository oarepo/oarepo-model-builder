from pathlib import Path

from . import process
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class JSONSchemaBuilder(JSONBaseBuilder):
    TYPE = "jsonschema"
    output_file_type = "jsonschema"
    output_file_name = "schema-file"
    parent_module_root_name = "jsonschemas"

    @process("**", condition=lambda current, stack: stack.schema_valid)
    def model_element(self):
        if isinstance(self.stack.top.data, dict) and not self.stack.top.data.get(
            "jsonschema", {}
        ).get("generate", True):
            # do not build the element if it should not be generated
            return
        self.model_element_enter()
        self.build_children()
        self.merge_jsonschema(self.stack.top.data)
        self.model_element_leave()

    def merge_jsonschema(self, data):
        if isinstance(data, dict) and "jsonschema" in data:
            jsonschema = self.call_components(
                "before_merge_jsonschema", data["jsonschema"], stack=self.stack
            )
            jsonschema.pop("generate", None)
            self.output.merge_jsonschema(jsonschema)

    def on_enter_model(self, output_name):
        self.output.primitive("type", "object")
        self.merge_jsonschema(self.stack.top.data)
        ensure_parent_modules(
            self.builder, Path(output_name), ends_at=self.parent_module_root_name
        )

    # def on_leave_model(self):
    #     self.check_and_output_required()
