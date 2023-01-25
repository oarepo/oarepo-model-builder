from oarepo_model_builder.utils.jinja import split_package_base_name

from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioCliSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_cli_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        cli_function = split_package_base_name(self.current_model.cli_function)

        output.add_entry_point(
            "flask.commands",
            self.current_model.flask_commands_setup_cfg,
            f"{'.'.join(cli_function[:-1])}:{cli_function[-1]}",
        )
