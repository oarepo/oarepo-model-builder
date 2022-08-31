from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput
from ..utils.verbose import log


class SetupCfgBuilder(OutputBuilder):
    TYPE = "setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        output.setdefault('metadata', 'name', self.settings.package_base.replace("_", "-"))
        output.setdefault('metadata', 'version', self.settings.get('version', '1.0.0dev1'))
        output.setdefault('metadata', 'description', f"A sample application for {self.settings.package}")
        output.setdefault('metadata', 'authors', '')

        # output.setdefault(
        #     "build-system",
        #     "requires",
        #     ["poetry-core>=1.0.8"],
        #     "build-backend",
        #     "poetry.core.masonry.api",
        # )

        output.setdefault('options', 'python', '>=3.9')

        if "runtime-dependencies" in self.schema:
            for dep, value in self.schema.runtime_dependencies.items():
                output.add_dependency(dep, '>=' + value)

        if "dev-dependencies" in self.schema:
            for dep, value in self.schema.dev_dependencies.items():
                output.add_dependency(dep, '>=' + value, group='options.extras_require', section='devs')

        if output.created:
            log(
                log.INFO,
                f"""To install the data model, run
    poetry install -E {self.settings.package}            
            """,
            )
