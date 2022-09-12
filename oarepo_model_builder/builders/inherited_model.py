from pathlib import Path

from . import process, OutputBuilder
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules
from ..outputs.cfg import CFGOutput


class InheritedModelBuilder(JSONBaseBuilder):
    TYPE = "inherited_model"
    output_file_type = "json"
    output_file_name = "inherited-model-file"
    parent_module_root_name = "models"

    @process("**")
    def model_element(self):
        self.model_element_enter()
        self.build_children()
        self.model_element_leave()

    def enter_model(self):
        # remove the special json base builder functionality
        # TODO: better handling for this
        pass

    def output_primitive(self, top, data):
        if data is not None:
            if not isinstance(data, (str, float, int, bool)):
                data = str(data)
        if top.key == "for-inheritance":
            return
        return super().output_primitive(top, data)

    def begin(self, schema, settings):
        super().begin(schema, settings)

        output_name = self.settings[self.output_file_name]
        self.output = self.builder.get_output(self.output_file_type, output_name)

        ensure_parent_modules(
            self.builder, Path(output_name), ends_at=self.parent_module_root_name
        )

    def finish(self):
        # force clean output
        self.output.force_clean_output()
