from pathlib import Path

from oarepo_model_builder.datatypes import DataType, datatypes

from ..outputs.cfg import CFGOutput
from . import OutputBuilder, process
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class ModelSaverBuilder(JSONBaseBuilder):
    TYPE = "model_saver"
    output_file_type = "json"
    output_file_name = "saved-model-file"
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

    def model_element_enter(self):
        super().model_element_enter()
        if self.stack.top.schema_element_type in ("items", "property"):
            datatype: DataType = datatypes.get_datatype(
                self.stack.top.data,
                self.stack.top.key,
                self.current_model,
                self.whole_schema,
                self.stack,
            )
            if datatype:
                marshmallow = datatype.marshmallow()
                marshmallow.setdefault("imports", []).extend(
                    [
                        {"import": imp.import_path, "alias": imp.alias}
                        if imp.alias
                        else {
                            "import": imp.import_path,
                        }
                        for imp in datatype.imports()
                    ]
                )
                self.output.merge(
                    {
                        "marshmallow": marshmallow,
                    }
                )

    def output_primitive(self, top, data):
        if data is not None:
            if not isinstance(data, (str, float, int, bool)):
                data = str(data)
        return super().output_primitive(top, data)

    def begin(self, schema, settings):
        super().begin(schema, settings)

        output_name = self.current_model[self.output_file_name]
        self.output = self.builder.get_output(self.output_file_type, output_name)
        self.output.enter(self.whole_schema.model_field, {"type": "object"})
        ensure_parent_modules(
            self.builder, Path(output_name), ends_at=self.parent_module_root_name
        )

    def finish(self):
        self.output.leave()
        # force clean output
        super().finish()
        self.output.force_clean_output()


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
