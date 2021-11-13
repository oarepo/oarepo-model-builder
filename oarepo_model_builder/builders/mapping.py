from ..outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.utils.stack import ModelBuilderStack
from . import OutputBuilder, on_enter, on_primitive, on_leave
from ..utils.schema import is_schema_element


class MappingBuilder(OutputBuilder):
    output_builder_type = 'mapping'

    @on_enter('/model/**')
    def enter_model_element(self, stack: ModelBuilderStack):
        if is_schema_element(stack):
            self.output.enter(stack.top.key, [] if stack.top_type == stack.LIST else {})
        else:
            # not a schema element, so ignore it and the whole subtree
            self.output.enter(stack.top.key, JSONSchemaOutput.IGNORE_SUBTREE)

    @on_primitive('/model/**')
    def primitive_model(self, stack: ModelBuilderStack):
        if is_schema_element(stack):
            self.output.primitive(stack.top.key, stack.top.el)

    @on_leave('/model/**')
    def leave_model_element(self, stack: ModelBuilderStack):
        if is_schema_element(stack):
            top = stack.top.el
            if 'oarepo:mapping' in top:
                self.output.merge_mapping(top['oarepo:mapping'])
        self.output.leave()

    @on_enter('/model')
    def enter_model(self, stack: ModelBuilderStack):
        self.output = self.builder.get_output('mapping', stack[0]['mapping-file'])
