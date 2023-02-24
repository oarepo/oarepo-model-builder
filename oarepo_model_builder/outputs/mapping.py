from .json import JSONOutput


class MappingOutput(JSONOutput):
    TYPE = "mapping"

    def merge_mapping(self, mapping):
        self.stack.merge(mapping)

    def replace_mapping(self, mapping):
        type_ = self.stack.real_top.get("type")
        if type_:
            mapping = {"type": type_, **mapping}
        self.stack.replace(mapping)
