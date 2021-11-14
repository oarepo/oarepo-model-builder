import os
from pathlib import Path

from . import ModelTransformer


class DefaultValuesTransformer(ModelTransformer):
    def transform(self, schema):
        if not schema.get('package'):
            package_name = os.path.basename(os.getcwd()).replace('-', '_')
            schema.set('package', package_name)
        if not schema.get('kebap-package'):
            schema.set('kebap-package', schema.get('package').replace('_', '-'))
        if not schema.get('package-path'):
            package_path = schema.get('package').split('.')
            schema.set('package-path',
                       Path(package_path[0]).joinpath(*package_path[1:]))
        if not schema.get('schema-version'):
            schema.set('schema-version', '1.0.0')
        if not schema.get('schema-name'):
            schema.set('schema-name', f"{schema.get('kebap-package')}-{schema.get('schema-version')}.json")
        if not schema.get('schema-file'):
            schema.set('schema-file',
                       os.path.join(
                           schema.get('package-path'),
                           'jsonschemas',
                           schema.get('schema-name')
                       ))
        if not schema.get('mapping-file'):
            schema.set('mapping-file',
                       os.path.join(
                           schema.get('package-path'),
                           'mappings',
                           'v7',
                           schema.get('schema-name')
                       ))
