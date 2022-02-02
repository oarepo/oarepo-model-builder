from pathlib import Path

from oarepo_model_builder.stack import ModelBuilderStack

from ..utils.schema import is_schema_element
from ..utils.verbose import log
from . import process
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class MappingBuilder(JSONBaseBuilder):
    TYPE = "mapping"
    output_file_type = "mapping"
    output_file_name = "mapping-file"
    parent_module_root_name = "mappings"

    @process("/model/**", condition=lambda current, stack: is_schema_element(stack))
    def enter_model_element(self):
        # ignore schema leaves different than "type" - for example, minLength, ...
        # that should not be present in mapping
        if (
            self.stack.top_type in (self.stack.LIST, self.stack.DICT)
            or
            # ignore top-level type=object as it is not allowed
            # in elasticsearch mapping (it is object automatically)
            self.stack.level > 3
            and self.stack.top.key == "type"
        ):

            self.model_element_enter()

            # process children
            self.build_children()

            data = self.stack.top.data
            if isinstance(data, dict) and "oarepo:mapping" in data:
                mapping = self.call_components("before_merge_mapping", data["oarepo:mapping"], stack=self.stack)
                self.output.merge_mapping(mapping)

            self.model_element_leave()

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
