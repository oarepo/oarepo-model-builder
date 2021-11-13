from ..outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.utils.stack import ModelBuilderStack
from . import OutputBuilder, on_enter, on_primitive, on_leave


class JSONSchemaBuilder(OutputBuilder):
    output_builder_type = 'jsonschema'

    """
        Alternativni moznost misto enter/leave, chce vyzkoumat 
        
        @on_element('/model/**')
        def model_element(self, stack: ModelBuilderStack):
            if self.is_schema_element(stack):
                self.output.enter(stack.top.key, [] if stack.top_type == stack.LIST else {})
            else:
                # not a schema element, so ignore it and the whole subtree
                self.output.enter(stack.top.key, JSONSchemaOutput.IGNORE_SUBTREE)
            
            yield                   # tady se resi podelementy
            
            self.output.leave()
    """

    @on_enter('/model/**')
    def enter_model_element(self, stack: ModelBuilderStack):
        if self.is_schema_element(stack):
            self.output.enter(stack.top.key, [] if stack.top_type == stack.LIST else {})
        else:
            # not a schema element, so ignore it and the whole subtree
            self.output.enter(stack.top.key, JSONSchemaOutput.IGNORE_SUBTREE)

    @on_primitive('/model/**')
    def primitive_model(self, stack: ModelBuilderStack):
        if self.is_schema_element(stack):
            self.output.primitive(stack.top.key, stack.top.el)

    @on_leave('/model/**')
    def leave_model_element(self, stack: ModelBuilderStack):
        self.output.leave()

    @on_enter('/model')
    def enter_model(self, stack: ModelBuilderStack):
        self.output = self.builder.get_output('jsonschema', stack[0]['schema-file'])

    @classmethod
    def is_schema_element(cls, stack: ModelBuilderStack):
        key = stack.top.key
        if not isinstance(key, str):
            return True
        if not key.startswith('oarepo:'):
            return True
        # if the key starts with oarepo:, it still might be in properties section
        if stack[-2].key == 'properties':
            return True
        return False
