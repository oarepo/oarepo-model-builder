from . import process
from .json_base import JSONBaseBuilder


class ExtendBuilder(JSONBaseBuilder):
    TYPE = "extend"
    output_file_type = "json"

    @process("**")
    def model_element(self):
        self.model_element_enter()
        self.build_children()
        self.model_element_leave()

    def enter_model(self):
        # build children are handled in model_element, so no default handling here
        pass

    def output_primitive(self, top, data):
        if data is not None and not isinstance(data, (str, float, int, bool)):
            data = str(data)
        return super().output_primitive(top, data)

    def begin(self, schema, settings):
        super(JSONBaseBuilder, self).begin(schema, settings)
        self.output = self.builder.get_output(self.output_file_type, "model.json5")
        self.output.primitive("type", "object")

    def finish(self):
        # force clean output
        super().finish()
        self.output.force_clean_output()
