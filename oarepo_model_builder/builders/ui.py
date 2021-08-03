import copy
import os

import click

from oarepo_model_builder.builders.json import JSONBuilder
from oarepo_model_builder.outputs.toml_output import TomlOutput
from oarepo_model_builder.outputs.ui import UIOutput


class UIBuilder(JSONBuilder):
    """Handles building of jsonschema from a data model specification."""

    def __init__(self):
        super().__init__()
        self.output = None

    def is_property(self, path):
        return len(path) > 1 and path[-2] == 'properties'  # TODO: tohle neni uplne spravne

    def begin(self, config, outputs, root):
        output = outputs['ui'] = UIOutput(path=config.resolve_path(
            'ui_path',
            '{package}/oarepo_ui/{datamodel}-v{datamodel_version}.json'))
        if 'poetry' not in outputs:
            pyproject = outputs['pyproject'] = TomlOutput(
                config.resolve_path('pyproject_path', 'pyproject.toml'))
        else:
            pyproject = outputs['pyproject']

        pyproject.add(
            'tool.poetry.plugins.oarepo_ui',
            config.datamodel,
            os.path.relpath(
                config.resolve_path(
                    'ui_path',
                    '{package}/oarepo_ui:{datamodel}-v{datamodel_version}.json'),
                config.base_dir).replace('/', '.')
        )

        self.stack[0] = output.data
        if 'oarepo:ui' in root:
            self.stack[-1].update(root['oarepo:ui'])  # title etc
        self.push({}, ['fields'])

    def pre(self, el, config, path, outputs):
        if self.is_property(path):
            self.push(copy.deepcopy(el.get('oarepo:ui', {})), path)
        else:
            self.push(self.IGNORED_NODE, path)  # ignored node means that just the node is output, not the whole subtree

    def post(self, el, config, path, outputs):
        self.pop()

    def end(self, config, outputs, root):
        self.pop()

    def options(self):
        return [
            click.option('ui-path'),
            click.option('pyproject-path')
        ]
