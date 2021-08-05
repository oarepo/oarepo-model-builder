from typing import List, Dict

import click

from oarepo_model_builder.builders import JSONBuilder
from oarepo_model_builder.config import Config
from oarepo_model_builder.outputs import JsonSchemaOutput, BaseOutput


class JSONSchemaBuilder(JSONBuilder):
    """Handles building of jsonschema from a data model specification."""

    def __init__(self):
        super().__init__()
        self.output = None

    def begin(self, config, outputs, root):
        output = outputs['jsonschema'] = JsonSchemaOutput()
        output.path = config.resolve_path(
            'schema_path',
            'jsonschemas/{package}/{datamodel}-v{datamodel_version}.json')
        self.stack[0] = output.data

    def pre(self, el, config: Config, path: List[str], outputs: Dict[str, BaseOutput]):
        path_skipped = path[-1].startswith('oarepo:')
        if path_skipped:
            self.push(self.IGNORED_SUBTREE, path)
        elif isinstance(el, dict):
            self.push({}, path)
        else:
            self.push(el, path)

    def post(self, el, config, path, outputs):
        self.pop()

    def options(self):
        return [
            click.option('schema-path')
        ]
