from oarepo_model_builder.builders.json import JSONBuilder
from oarepo_model_builder.output import JsonSchemaOutput


class JSONSchemaBuilder(JSONBuilder):
    """Handles building of jsonschema from a data model specification."""
    def __init__(self):
        super().__init__()
        self.output = None

    def pre(self, el, config, path, outputs):
        if not path:
            output = outputs['jsonschema'] = JsonSchemaOutput("TODO")
            self.stack[0] = output.data
        else:
            path_skipped = path[-1].startswith('oarepo:')
            if path_skipped:
                self.push(self.IGNORED, path)
            elif isinstance(el, dict):
                self.push({}, path)
            elif isinstance(el, (list, tuple)):
                self.push([], path)
            else:
                self.push(el, path)

    def post(self, el, config, path, outputs):
        self.pop()
