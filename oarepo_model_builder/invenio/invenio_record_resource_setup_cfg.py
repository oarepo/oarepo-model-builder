from oarepo_model_builder.utils.jinja import split_package_base_name

from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordResourceSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_resource_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        register_function = split_package_base_name(
            self.current_model.definition["api-blueprint"]["function"]
        )

        output.add_entry_point(
            "invenio_base.api_blueprints",
            self.current_model.definition["api-blueprint"]["alias"],
            f"{register_function[0]}:{register_function[-1]}",
        )

        register_function = split_package_base_name(
            self.current_model.definition["app-blueprint"]["function"]
        )

        output.add_entry_point(
            "invenio_base.blueprints",
            self.current_model.definition["app-blueprint"]["alias"],
            f"{register_function[0]}:{register_function[-1]}",
        )
