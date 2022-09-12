from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput
from ..outputs.toml import TOMLOutput
from ..utils.verbose import log


class PyprojectTOMLBuilder(OutputBuilder):
    TYPE = "pyproject_toml"

    def finish(self):
        super().finish()
        output: TOMLOutput = self.builder.get_output("toml", "pyproject.toml")
        output.setdefault(
            "build_system", "requires", ["setuptools", "wheel", "babel>2.8"]
        )
        output.setdefault("build_system", "build-backend", "setuptools.build_meta")
