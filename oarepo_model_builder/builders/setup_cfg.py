from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput
from ..utils.verbose import log
from pkg_resources import parse_version


class SetupCfgBuilder(OutputBuilder):
    TYPE = "setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        output.setdefault('metadata', 'name', self.settings.package_base.replace("_", "-"))
        version = self.schema.get('version', '1.0.0dev1')
        output.setdefault('metadata', 'version', version)
        if parse_version(output.get('metadata', 'version').value) < parse_version(version):
            output.set('metadata', 'version', version)
        output.setdefault('metadata', 'description', f"A sample application for {self.settings.package}")
        output.setdefault('metadata', 'authors', '')

        output.setdefault('options', 'python', '>=3.9')

        output.add_dependency("invenio_access", ">=1.4.4")
        output.add_dependency("invenio_app", ">=1.3.4")
        output.add_dependency("invenio_db", ">=1.0.14")
        output.add_dependency("invenio_pidstore", ">=1.2.3")
        output.add_dependency("invenio_records", ">=1.7.4")
        output.add_dependency("invenio_records_permissions", ">=0.13.0")
        output.add_dependency("invenio_records_resources", ">=0.20.1")

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
