from oarepo_model_builder.utils.jinja import package_name

from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioRecordMetadataModelsSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_metadata_models_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        metadata_package = package_name(self.current_model.record_metadata_class)

        output.add_entry_point(
            "invenio_db.models",
            self.current_model.record_schema_metadata_setup_cfg,
            metadata_package,
        )
