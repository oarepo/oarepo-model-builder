from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput


class InvenioVersionBuilder(PythonBuilder):
    TYPE = "invenio_version"

    def finish(self):
        super().finish()

        python_output: PythonOutput = self.builder.get_output(
            "python", self.settings.package_path / "version.py"
        )
        python_output.merge("invenio_version", {"settings": self.settings})
