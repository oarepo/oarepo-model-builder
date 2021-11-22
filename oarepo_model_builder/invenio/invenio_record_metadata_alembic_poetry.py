from ..builders import OutputBuilder
from ..builders.utils import ensure_parent_modules
from ..outputs.toml import TOMLOutput


class InvenioRecordMetadataAlembicPoetryBuilder(OutputBuilder):
    TYPE = 'invenio_record_metadata_alembic_poetry'

    def finish(self):
        super().finish()

        output: TOMLOutput = self.builder.get_output(
            'toml',
            'pyproject.toml'
        )
        output.set("tool.poetry.plugins.'invenio_db.alembic'",
                   self.settings.python.record_schema_metadata_alembic,
                   f'{self.settings.package}:alembic'
                   )

        python_path = self.settings.package_path / 'alembic' / '__init__.py'
        # create parent modules if they do not exist
        ensure_parent_modules(
            self.builder,
            python_path,
            max_depth=len(python_path.parts)
        )

        # and create empty __init__.py
        self.builder.get_output(
            'python',
            python_path
        )
