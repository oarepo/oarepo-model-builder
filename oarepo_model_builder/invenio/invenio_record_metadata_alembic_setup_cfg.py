from pathlib import Path

from ..builders import OutputBuilder
from ..builders.utils import ensure_parent_modules
from ..outputs.cfg import CFGOutput
from ..utils.python_name import module_to_path, split_package_base_name


class InvenioRecordMetadataAlembicSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_metadata_alembic_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        if "alembic" not in self.current_model.definition["record-metadata"]:
            return

        alembic_module_parent, alembic_module = split_package_base_name(
            self.current_model.definition["record-metadata"]["alembic"]
        )
        output.add_entry_point(
            "invenio_db.alembic",
            self.current_model.definition["record-metadata"]["alias"],
            f"{alembic_module_parent}:{alembic_module}",
        )

        python_path = (
            Path(
                module_to_path(
                    self.current_model.definition["record-metadata"]["alembic"]
                )
            )
            / "__init__.py"
        )
        # create parent modules if they do not exist
        ensure_parent_modules(
            self.builder, python_path, max_depth=len(python_path.parts)
        )

        # and create empty __init__.py
        self.builder.get_output("python", python_path)
