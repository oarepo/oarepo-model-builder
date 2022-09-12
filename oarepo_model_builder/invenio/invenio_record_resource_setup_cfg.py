from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordResourceSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_resource_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        register_function = self.settings.python.create_blueprint_from_app.rsplit(
            ".", maxsplit=1
        )

        output.add_entry_point(
            "invenio_base.api_blueprints",
            self.settings.python.record_resource_blueprint_name,
            f"{register_function[0]}:{register_function[-1]}",
        )
