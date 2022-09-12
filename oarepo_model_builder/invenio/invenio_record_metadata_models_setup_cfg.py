from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordMetadataModelsSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_metadata_models_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        metadata_package = self.settings.python.record_metadata_class.rsplit(
            ".", maxsplit=1
        )[0]

        output.add_entry_point(
            "invenio_db.models",
            self.settings.python.record_schema_metadata_setup_cfg,
            metadata_package,
        )
