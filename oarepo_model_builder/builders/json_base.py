from oarepo_model_builder.builders import OutputBuilder, process
from oarepo_model_builder.utils.stack import ModelBuilderStack


class JSONBaseBuilder(OutputBuilder):
    def model_element_enter(self, stack: ModelBuilderStack):
        top = stack.top
        match stack.top_type:
            case stack.PRIMITIVE:
                self.output.primitive(top.key, top.data)
            case stack.LIST:
                self.output.enter(top.key, [])
            case stack.DICT:
                self.output.enter(top.key, {})

    def model_element_leave(self, stack: ModelBuilderStack):
        if stack.top_type != stack.PRIMITIVE:
            self.output.leave()

    @process('/model')
    def enter_model(self, stack: ModelBuilderStack):
        self.output = self.builder.get_output(self.output_file_type, stack[0][self.output_file_name])
