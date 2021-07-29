import copy

from oarepo_model_builder.builders.json import JSONBuilder
from oarepo_model_builder.output import JsonSchemaOutput, BaseOutput


class UIOutput(BaseOutput):
    output_type = 'ui'

    def __init__(self, path):
        super().__init__(path, {})


class UIBuilder(JSONBuilder):
    """Handles building of jsonschema from a data model specification."""

    def __init__(self):
        super().__init__()
        self.output = None

    def is_property(self, path):
        return len(path) > 1 and path[-2] == 'properties'   # TODO: tohle neni uplne spravne

    def pre(self, el, config, path, outputs):
        if not path:
            output = outputs['ui'] = UIOutput("TODO")
            self.stack[0] = output.data
            if 'oarepo:ui' in el:
                self.stack[-1].update(el['oarepo:ui'])  # title etc
        elif self.is_property(path):
            self.push(copy.deepcopy(el.get('oarepo:ui', {})), path)
        else:
            self.push(self.IGNORED_NODE, path)      # ignored node means that just the node is output, not the whole subtree

    def post(self, el, config, path, outputs):
        self.pop()
