from oarepo_model_builder.builders.json import JSONBuilder


class JSONSchemaBuilder(JSONBuilder):
    """Handles building of jsonschema from a data model specification."""

    def pre(self, el, config, path, outputs):
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
