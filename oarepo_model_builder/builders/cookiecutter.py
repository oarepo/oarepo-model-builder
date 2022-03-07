from datetime import date
from pathlib import Path

from os.path import basename
from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.builders.utils import ensure_directory
from ..utils.verbose import log
from cookiecutter.main import cookiecutter
from invenio_cli.helpers.cookiecutter_wrapper import CookiecutterWrapper
from invenio_cli.helpers.cli_config import CLIConfig


class CookiecutterBuilder(OutputBuilder):
    TYPE = "cookiecutter"

    def _generate_sample_site(self, app_package_path):
        package = self.schema.settings.package.replace('_', '-')
        template = 'gh:oarepo/cookiecutter-oarepo-instance'
        checkout = 'dev1'
        flavour = 'oarepo'

        builder = CookiecutterWrapper(
            flavour,
            **{
                'checkout': checkout,
                'no_input': True
            })
        builder.template_name = builder.extract_template_name(template)
        config_file = builder.create_and_dump_config_file()

        log.enter(log.INFO, 'Running cookiecutter...')
        project_dir = cookiecutter(
            template,
            checkout='dev1',
            config_file=config_file,
            overwrite_if_exists=True,
            no_input=True,
            extra_context=dict(
                project_name=f"{package} Sample site",
                project_shortname=f"{package}-sample-site",
                project_site="oarepo.org",
                github_repo=f"oarepo/{package}-sample-site",
                description=f"Testing OARepo Site instance for {package} datamodel.",
                author_name="CESNET",
                author_email="info@oarepo.org",
                year=f"{date.today().year}",
                python_version="3.9",
                database="postgresql",
                elasticsearch="7",
                file_storage="S3",
                development_tools="yes",
                app_package=f"{package}-sample-app",
                app_package_path=f"../{app_package_path}",
                # datamodel_package=package,
                # datamodel_package_path="../"
            )
        )
        saved_replay = builder.get_replay()
        CLIConfig.write(project_dir, flavour, saved_replay)
        log.leave(
            log.INFO, "Generated sample oarepo site in %s", project_dir)
        ensure_directory(self.builder, f"{Path(project_dir)}/logs")

    def _generate_sample_app(self):
        package = self.schema.settings.package.replace('_', '-')
        template = 'gh:oarepo/cookiecutter-oarepo-app'
        checkout = 'dev1'
        log.enter(log.INFO, 'Running cookiecutter...')
        project_dir = cookiecutter(
            template,
            checkout=checkout,
            overwrite_if_exists=True,
            no_input=True,
            extra_context=dict(
                project_name=f"{package} Sample app",
                project_shortname=f"{package}-sample-app",
                project_site="oarepo.org",
                github_repo=f"oarepo/{package}-sample-app",
                description=f"Testing OARepo application module with {package} datamodel.",
                author_name="CESNET",
                author_email="info@oarepo.org",
                year=f"{date.today().year}",
                python_version="3.9",
                database="postgresql",
                elasticsearch="7",
                file_storage="S3",
                development_tools="yes",
            )
        )
        log.leave(
            log.INFO, "Generated sample application in %s", project_dir)

        return basename(project_dir)

    def finish(self):
        super().finish()

        if (self.schema.settings.get('no-cookiecutter')):
            return

        app_project_dir = self._generate_sample_app()
        self._generate_sample_site(app_project_dir)
