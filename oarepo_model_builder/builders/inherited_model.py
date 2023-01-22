from pathlib import Path
from oarepo_model_builder.datatypes import datatypes, DataType

from oarepo_model_builder.stack.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge

from ..outputs.cfg import CFGOutput
from . import OutputBuilder, process
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class InheritedModelBuilder(JSONBaseBuilder):
    TYPE = "inherited_model"
    output_file_type = "json"
    output_file_name = "inherited-model-file"
    parent_module_root_name = "models"

    @process("**")
    def model_element(self):
        if self.stack.top.schema_element_type in ("property", "items"):
            data = self.stack.top.data
            if "type" in data:
                datatype: DataType = datatypes.get_datatype(data)
                if datatype:
                    deepmerge(data.setdefault("jsonschema", {}), datatype.json_schema())
                    deepmerge(data.setdefault("mapping", {}), datatype.mapping())
                    marshmallow = data.setdefault("marshmallow", {})
                    deepmerge(marshmallow, datatype.marshmallow())

                    marshmallow.setdefault("imports", []).extend(
                        [
                            {"import": imp.import_path, "alias": imp.alias}
                            if imp.alias
                            else {"import": imp.import_path}
                            for imp in datatype.imports()
                        ]
                    )
                    if "schema-class" in marshmallow:
                        marshmallow["schema-base-classes"] = [
                            marshmallow.pop("schema-class")
                        ]
        self.model_element_enter()
        self.build_children()
        self.model_element_leave()

    def enter_model(self):
        pass

    @process("/output-directory/**", priority=10)
    def remove_output_directory(self):
        return

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
