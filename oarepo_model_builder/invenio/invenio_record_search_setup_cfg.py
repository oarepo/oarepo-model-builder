from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordSearchSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_search_setup_cfg"

    def finish(self):
        super().finish()
        if self.current_model.definition["mapping"].get("skip"):
            return

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_entry_point(
            "invenio_search.mappings",
            self.current_model.definition["mapping"]["alias"],
            self.current_model.definition["mapping"]["module"],
        )
