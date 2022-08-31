from ..builders import OutputBuilder
from ..outputs.cfg import CFGOutput


class InvenioSampleAppSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_sample_app_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_dependency('invenio', '>=3.5.0a3',
                              extras=["base", "auth", "metadata", "files", "postgresql", "elasticsearch7"])

        output.add_dependency('pyyaml', '>=6', group='options.extras_require', section='sample-app')

        output.add_dependency('invenio-rest', '>=1.2.8', group='options.extras_require', section='sample-app')

        output.add_dependency('invenio-records-resources', '>=0.20.1', group='options.extras_require',
                              section='sample-app')
