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

        if element_type == "items":
            # do not output "items" container
            self.build_children()
            self.set_searchable()
            self.merge_mapping(self.stack.top.data)

        elif element_type in ("properties", "property"):
            self.index_enabled_stack.append(
                self.stack.top.data.get("facets", {}).get(
                    "searchable", self.index_enabled_stack[-1]
                )
            )
            self.children_indexed.append(False)

            self.model_element_enter()

            # process children
            self.build_children()
            if element_type == "property":
                self.set_searchable()

            self.merge_mapping(self.stack.top.data)

            self.model_element_leave()

            self.index_enabled_stack.pop()
            self.children_indexed.pop()

        elif element_type == "type" and self.stack.top.data != "array":
            # do not output "type=array"
            self.model_element_enter()
            self.model_element_leave()

    def set_searchable(self):
        if self.stack.top.data.type != "array":
            if self.stack.top.data.type in ("object", "nested"):
                searchable = self.children_indexed[-1]
                if not searchable:
                    self.stack.top.data.setdefault("mapping", {})["enabled"] = False
            else:
                searchable = self.index_enabled_stack[-1] or self.children_indexed[-1]
                if not searchable:
                    self.stack.top.data.setdefault("mapping", {})["index"] = False
                else:
                    for idx in range(0, len(self.children_indexed)):
                        self.children_indexed[idx] = True

    def merge_mapping(self, data):
        if isinstance(data, dict) and "mapping" in data:
            mapping = self.call_components(
                "before_merge_mapping", data["mapping"], stack=self.stack
            )
            if not mapping.get("enabled", True):
                self.output.replace_mapping(mapping)
            else:
                self.output.merge_mapping(mapping)

    def on_enter_model(self, output_name):
        self.index_enabled_stack = [self.current_model.get("searchable", True)]
        self.children_indexed = [False]
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
