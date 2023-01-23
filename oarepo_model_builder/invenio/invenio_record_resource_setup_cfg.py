from oarepo_model_builder.utils.jinja import split_package_base_name

from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordResourceSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_resource_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        register_function = split_package_base_name(
            self.model.create_blueprint_from_app
        )

        output.add_entry_point(
            "invenio_base.api_blueprints",
            self.model.record_resource_blueprint_name,
            f"{register_function[0]}:{register_function[-1]}",
        )
