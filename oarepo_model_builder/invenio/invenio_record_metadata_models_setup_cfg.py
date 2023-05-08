from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordMetadataModelsSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_metadata_models_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_entry_point(
            "invenio_db.models",
            self.current_model.definition["record-metadata"]["alias"],
            self.current_model.definition["record-metadata"]["module"],
        )
