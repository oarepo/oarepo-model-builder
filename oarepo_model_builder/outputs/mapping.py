from .json import JSONOutput


class MappingOutput(JSONOutput):
    output_type = 'mapping'

    def merge_mapping(self, mapping):
        self.stack.merge(mapping)

