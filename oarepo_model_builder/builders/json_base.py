from oarepo_model_builder.builders import OutputBuilder, process
from oarepo_model_builder.stack import ModelBuilderStack


class JSONBaseBuilder(OutputBuilder):
    output_file_name: str = None
    output_file_type: str = None
    parent_module_root_name: str = None

    def model_element_enter(self):
        top = self.stack.top
        data = top.data
        data = self.call_components("model_element_enter", data, stack=self.stack)
        if self.stack.top_type == self.stack.PRIMITIVE:
            self.output_primitive(top, data)
        elif self.stack.top_type == self.stack.LIST:
            self.output.enter(top.key, [])
        elif self.stack.top_type == self.stack.DICT:
            self.output.enter(top.key, {})

    def output_primitive(self, top, data):
        self.output.primitive(top.key, data)

    def model_element_leave(self):
        self.call_components(
            "model_element_leave", self.stack.top.data, stack=self.stack
        )
        if self.stack.top_type != self.stack.PRIMITIVE:
            self.output.leave()

    @process("/model")
    def enter_model(self):
        output_name = self.settings[self.output_file_name]
        self.output = self.builder.get_output(self.output_file_type, output_name)
        self.on_enter_model(output_name)
        self.build_children()
        self.on_leave_model()

    def on_enter_model(self, output_name):
        pass

    def on_leave_model(self):
        pass
