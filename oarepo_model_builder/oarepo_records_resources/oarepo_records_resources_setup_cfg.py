from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class OarepoRecordsResourcesSetupCfgBuilder(OutputBuilder):
    TYPE = "oarepo_records_resources_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        if getattr(self.schema, "expandable_fields", None):
            output.add_dependency("oarepo-records-resources", ">=1.0.0")
