from pathlib import Path

from ..outputs.cfg import CFGOutput
from . import OutputBuilder
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class ModelSaverBuilder(JSONBaseBuilder):
    TYPE = "model_saver"
    output_file_type = "json"
    output_file_name = "saved-model-file"
    parent_module_root_name = "models"

    def build_node(self, node):
        generated = self.generate(node)
        self.output.merge({"model": generated})

    def generate(self, node):
        section: Section = node.section_model_saver
        ret = {**node.definition}
        ret.pop("properties", None)
        ret.pop("items", None)
        ret.update(**section.config)

        if section.children:
            properties = ret.setdefault("properties", {})
            for k, v in section.children.items():
                v = self.generate(v)
                properties[k] = v
        if section.item:
            ret["items"] = self.generate(section.item)
        return ret

    def begin(self, schema, settings):
        super().begin(schema, settings)

        output_name = self.current_model.definition[self.output_file_name]
        self.output = self.builder.get_output(self.output_file_type, output_name)
        ensure_parent_modules(
            self.builder, Path(output_name), ends_at=self.parent_module_root_name
        )


class ModelRegistrationBuilder(OutputBuilder):
    TYPE = "model_registration"

    def finish(self):
        super().finish()
        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        output.add_entry_point(
            "oarepo.models",
            self.current_model.oarepo_models_setup_cfg,
            f"{self.current_model.package}.models:{Path(self.current_model.saved_model_file).name}",
        )
