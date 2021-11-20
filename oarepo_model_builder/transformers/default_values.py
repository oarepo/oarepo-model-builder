import os
from pathlib import Path
from typing import Dict

from . import ModelTransformer
from ..schema import ModelSchema


class DefaultValuesTransformer(ModelTransformer):
    def transform(self, schema: ModelSchema, settings: Dict):

        if not settings.get('package'):
            package_name = os.path.basename(os.getcwd()).replace('-', '_')
            settings['package'] = package_name

        if not settings.get('kebap-package'):
            settings['kebap-package'] = settings['package'].replace('_', '-')

        if not settings.get('package-path'):
            package_path = settings.get('package').split('.')
            settings['package-path'] = Path(package_path[0]).joinpath(*package_path[1:])

        if not settings.get('schema-version'):
            settings['schema-version'] = '1.0.0'

        if not settings.get('schema-name'):
            settings['schema-name'] = f"{settings.get('kebap-package')}-{settings.get('schema-version')}.json"

        if not settings.get('schema-file'):
            settings['schema-file'] = os.path.join(
                settings.get('package-path'),
                'jsonschemas',
                settings.get('schema-name')
            )

        if not settings.get('mapping-file'):
            settings['mapping-file'] = os.path.join(
                settings.get('package-path'),
                'mappings',
                'v7',
                settings.get('schema-name')
            )
