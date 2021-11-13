from oarepo_model_builder.utils.stack import ModelBuilderStack
from . import process
from .json_base import JSONBaseBuilder
from ..utils.schema import is_schema_element


class JSONSchemaBuilder(JSONBaseBuilder):
    output_builder_type = 'jsonschema'
    output_file_type = 'jsonschema'
    output_file_name = 'schema-file'

    @process('/model/**', condition=lambda current: is_schema_element(current.stack))
    def model_element(self, stack: ModelBuilderStack):
        self.model_element_enter(stack)
        yield
        self.model_element_leave(stack)
