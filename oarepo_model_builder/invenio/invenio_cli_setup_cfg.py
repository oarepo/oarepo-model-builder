from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioCliSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_cli_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        cli_function = self.settings.python.cli_function.rsplit(".", maxsplit=1)

        output.add_entry_point(
            "flask.commands",
            self.settings.kebap_package,
            f"{'.'.join(cli_function[:-1])}:{cli_function[-1]}",
        )
