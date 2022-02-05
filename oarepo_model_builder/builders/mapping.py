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

    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        # ignore schema leaves different than "type" - for example, minLength, ...
        # that should not be present in mapping
        if (
            self.stack.top_type in (self.stack.LIST, self.stack.DICT)
            or
            # ignore top-level type=object as it is not allowed
            # in elasticsearch mapping
            self.stack.level > 3
            and self.stack.top.key == "type"
        ):
            element_type = self.stack.top.schema_element_type
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
        if isinstance(data, dict) and "oarepo:mapping" in data:
            mapping = self.call_components("before_merge_mapping", data["oarepo:mapping"], stack=self.stack)
            self.output.merge_mapping(mapping)

    def on_enter_model(self, output_name):
        ensure_parent_modules(self.builder, Path(output_name), ends_at=self.parent_module_root_name)
        self.output.merge(self.settings.elasticsearch.templates[self.settings.elasticsearch.version])
        self.output.enter("mappings", {})

    def finish(self):
        super().finish()

        log(
            log.INFO,
            f"""
    invenio index init --force
            """,
        )
