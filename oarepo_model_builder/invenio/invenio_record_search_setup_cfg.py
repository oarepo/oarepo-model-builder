from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordSearchSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_search_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_entry_point(
            "invenio_search.mappings",
            self.current_model.record_mapping_setup_cfg,
            self.current_model.mapping_package,
        )
