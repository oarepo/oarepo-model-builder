from typing import List, Dict

from oarepo_model_builder.builders.json import JSONBuilder
from oarepo_model_builder.config import Config
from oarepo_model_builder.outputs.output import JsonSchemaOutput, BaseOutput


class JSONSchemaBuilder(JSONBuilder):
    """Handles building of jsonschema from a data model specification."""
    def __init__(self):
        super().__init__()
        self.output = None

    def pre(self, el, config: Config, path: List[str], outputs: Dict[str, BaseOutput]):
        if not path:
            output = outputs['jsonschema'] = JsonSchemaOutput(
                config.resolve_path('jsonschemas/{package}/{datamodel}-v{datamodel_version}.json',
                                    'schema_path')
            )
            self.stack[0] = output.data
        else:
            path_skipped = path[-1].startswith('oarepo:')
            if path_skipped:
                self.push(self.IGNORED_SUBTREE, path)
            elif isinstance(el, dict):
                self.push({}, path)
            elif isinstance(el, (list, tuple)):
                self.push([], path)
            else:
                self.push(el, path)

    def post(self, el, config, path, outputs):
        self.pop()