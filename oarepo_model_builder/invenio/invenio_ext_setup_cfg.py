from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioExtSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_ext_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        ext_class = self.settings.python.ext_class.rsplit(".", maxsplit=1)

        output.add_entry_point(
            "invenio_base.api_apps",
            self.settings.package,
            f"{ext_class[0]}:{ext_class[-1]}",
        )

        # need to add ext to apps because cli depends on it
        output.add_entry_point(
            "invenio_base.apps",
            self.settings.package,
            f"{ext_class[0]}:{ext_class[-1]}",
        )
