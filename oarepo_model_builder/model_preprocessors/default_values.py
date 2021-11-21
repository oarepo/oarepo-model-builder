import os
from pathlib import Path
from typing import Dict

from . import ModelPreprocessor
from ..schema import ModelSchema


class DefaultValuesModelPreprocessor(ModelPreprocessor):

    def transform(self, schema: ModelSchema, settings: Dict):
        self.set(settings, 'package', lambda: os.path.basename(os.getcwd()).replace('-', '_'))

        self.set(settings, 'kebap-package', lambda: settings.package.replace('_', '-'))

        @self.set(settings, 'package-path')
        def c():
            package_path = settings.package.split('.')
            return Path(package_path[0]).joinpath(*package_path[1:])

        self.set(settings, 'schema-version', lambda: '1.0.0')

        self.set(settings, 'schema-name', lambda: f"{settings.kebap_package}-{settings.schema_version}.json")

        self.set(
            settings, 'schema-file', lambda: os.path.join(
                settings.package_path,
                'jsonschemas',
                settings.schema_name
            )
        )

        self.set(
            settings, 'mapping-file', lambda: os.path.join(
                settings.package_path,
                'mappings',
                'v7',
                settings.schema_name
            )
        )
