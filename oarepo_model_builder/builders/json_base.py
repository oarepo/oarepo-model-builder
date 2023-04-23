from oarepo_model_builder.builders import OutputBuilder
from typing import Optional


class JSONBaseBuilder(OutputBuilder):
    output_file_name: str
    output_file_type: str
    parent_module_root_name: str

    def begin(self, current_model, schema):
        super().begin(current_model, schema)
        output_name = self.current_model.definition[self.output_file_name]
        self.output = self.builder.get_output(self.output_file_type, output_name)

    def finish(self):
        return super().finish()
