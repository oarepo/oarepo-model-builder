from pathlib import Path

from ..utils.verbose import log
from . import process
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class MappingBuilder(JSONBaseBuilder):
    TYPE = "mapping"
    output_file_type = "mapping"
    output_file_name = "mapping-file"
    parent_module_root_name = "mappings"

    @process("**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        # ignore schema leaves different than "type" - for example, minLength, ...
        # that should not be present in mapping
        element_type = self.stack.top.schema_element_type
        if element_type in ("properties", "property", "type", "items"):
            if element_type == "items":
                # do not output "items" container
                self.build_children()
                self.merge_mapping(self.stack.top.data)
                return
            elif element_type == "type" and self.stack.top.data == "array":
                # do not output "type=array"
                return

            self.model_element_enter()

            # process children
            self.build_children()

            self.merge_mapping(self.stack.top.data)

            self.model_element_leave()

    def merge_mapping(self, data):
        if isinstance(data, dict) and "mapping" in data:
            mapping = self.call_components(
                "before_merge_mapping", data["mapping"], stack=self.stack
            )
            self.output.merge_mapping(mapping)

    def on_enter_model(self, output_name):
        ensure_parent_modules(
            self.builder, Path(output_name), ends_at=self.parent_module_root_name
        )
        if "mapping" in self.current_model:
            if (
                "opensearch" not in self.settings
                or "version" not in self.settings.opensearch
            ):
                raise ValueError(
                    "Please define settings.opensearch.version (for example, to os-v2)"
                )
            self.output.merge(
                self.current_model.mapping[self.settings.opensearch.version]
            )
        self.output.enter("mappings", {})

    def finish(self):
        super().finish()

        log(
            log.INFO,
            f"""
    invenio index init --force
            """,
        )
