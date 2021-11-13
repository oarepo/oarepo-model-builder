from oarepo_model_builder.utils.stack import ModelBuilderStack
from . import process
from .json_base import JSONBaseBuilder
from ..utils.schema import is_schema_element


class MappingBuilder(JSONBaseBuilder):
    output_builder_type = 'mapping'
    output_file_type = 'mapping'
    output_file_name = 'mapping-file'

    @process('/model/**', condition=lambda current: is_schema_element(current.stack))
    def enter_model_element(self, stack: ModelBuilderStack):
        self.model_element_enter(stack)

        # process children
        yield

        data = stack.top.data
        if 'oarepo:mapping' in data:
            self.output.merge_mapping(data['oarepo:mapping'])

        self.model_element_leave(stack)
