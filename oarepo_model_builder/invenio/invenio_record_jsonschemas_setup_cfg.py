from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordJSONSchemasSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_jsonschemas_setup_cfg"

    def finish(self):
        super().finish()
        if self.current_model.definition["json-schema-settings"].get("skip"):
            return

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_entry_point(
            "invenio_jsonschemas.schemas",
            self.current_model.definition["json-schema-settings"]["alias"],
            self.current_model.definition["json-schema-settings"]["module"],
        )
