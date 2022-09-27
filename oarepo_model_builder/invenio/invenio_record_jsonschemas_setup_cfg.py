from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordJSONSchemasSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_jsonschemas_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_entry_point(
            "invenio_jsonschemas.schemas",
            self.settings.python.record_jsonschemas_setup_cfg,
            self.settings.jsonschemas_package,
        )
