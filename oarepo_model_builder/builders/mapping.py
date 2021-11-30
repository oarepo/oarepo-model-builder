from pathlib import Path

from oarepo_model_builder.stack import ModelBuilderStack
from . import process
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules
from ..utils.schema import is_schema_element
from ..utils.verbose import log


class MappingBuilder(JSONBaseBuilder):
    TYPE = 'mapping'
    output_file_type = 'mapping'
    output_file_name = 'mapping-file'
    parent_module_root_name = 'mappings'

    @process('/model/**', condition=lambda current: is_schema_element(current.stack))
    def enter_model_element(self, stack: ModelBuilderStack):
        # ignore schema leaves different than "type" - for example, minLength, ...
        # that should not be present in mapping
        if stack.top_type in (stack.LIST, stack.DICT) or stack.top.key == 'type':
            self.model_element_enter(stack)

            # process children
            yield

            data = stack.top.data
            if isinstance(data, dict) and 'oarepo:mapping' in data:
                self.output.merge_mapping(data['oarepo:mapping'])

            self.model_element_leave(stack)

    def on_enter_model(self, output_name, stack: ModelBuilderStack):
        ensure_parent_modules(self.builder, Path(output_name),
                              ends_at=self.parent_module_root_name)
        self.output.merge(
            self.settings.elasticsearch.templates[self.settings.elasticsearch.version]
        )
        self.output.enter('mappings', {})

        if self.settings.get('top_level_metadata'):
            self.output.enter('properties', {})
            self.output.enter('metadata', {})
            self.output.primitive('type', 'object')

    def finish(self):
        super().finish()

        log(log.INFO, f"""
    invenio index init --force
            """)