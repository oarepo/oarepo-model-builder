from ..outputs.python import PythonOutput
from .python import PythonBuilder


class SetupPyBuilder(PythonBuilder):
    TYPE = "setup_py"

    def finish(self):
        super().finish()

        python_output: PythonOutput = self.builder.get_output("python", "setup.py")
        python_output.merge(
            "setup_py", {"settings": self.settings, "current_model": self.current_model}
        )
