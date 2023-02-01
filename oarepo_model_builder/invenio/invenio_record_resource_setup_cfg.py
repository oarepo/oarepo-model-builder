from oarepo_model_builder.utils.jinja import split_package_base_name

from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordResourceSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_resource_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        register_function = split_package_base_name(
            self.current_model.create_blueprint_from_app
        )

        output.add_entry_point(
            "invenio_base.api_blueprints",
            self.current_model.record_api_blueprints_setup_cfg,
            f"{register_function[0]}:{register_function[-1]}",
        )
