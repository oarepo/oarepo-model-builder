import os
from pathlib import Path

from ..datatypes import Section
from ..outputs.cfg import CFGOutput
from ..utils.dict import dict_get
from . import OutputBuilder
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class ModelSaverBuilder(JSONBaseBuilder):
    TYPE = "model_saver"
    output_file_type = "json"
    output_file_name = ["saved-model", "file"]
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

    def begin(self, current_model, schema):
        super().begin(current_model, schema)

        output_name = dict_get(self.current_model.definition, self.output_file_name)
        self.output = self.builder.get_output(self.output_file_type, output_name)
        ensure_parent_modules(
            self.builder, Path(output_name), ends_at=self.parent_module_root_name
        )


class ModelRegistrationBuilder(OutputBuilder):
    TYPE = "model_registration"

    def finish(self):
        super().finish()
        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        module = self.current_model.definition["saved-model"]["module"]
        output.add_entry_point(
            "oarepo.models",
            self.current_model.definition["saved-model"]["alias"],
            f"{module}:{os.path.basename(self.current_model.definition['saved-model']['file'])}",
        )
