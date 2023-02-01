from oarepo_model_builder.utils.jinja import split_package_base_name

from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioExtSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_ext_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        package_name, base_name = split_package_base_name(self.current_model.ext_class)

        output.add_entry_point(
            "invenio_base.api_apps",
            self.current_model.extension_suffix,
            f"{package_name}:{base_name}",
        )

        # need to add ext to apps because cli depends on it
        output.add_entry_point(
            "invenio_base.apps",
            self.current_model.extension_suffix,
            f"{package_name}:{base_name}",
        )
