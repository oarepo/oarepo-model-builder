from ..utils.deepmerge import deepmerge
from .json_base import JSONBaseBuilder
from ..datatypes import Section, ModelDataType


def deep_searchable_enabled(dt):
    mapping = dt.section_mapping
    if mapping.section.get("enabled", None) is False:
        return False
    if mapping.item:
        return deep_searchable_enabled(mapping.item)
    for c in mapping.children.values():
        if not deep_searchable_enabled(c):
            return False
    return True


class MappingBuilder(JSONBaseBuilder):
    TYPE = "mapping"
    output_file_type = "mapping"
    output_file_name = "mapping-file"
    parent_module_root_name = "mappings"

    def build_node(self, node):
        generated = self.generate_model(node)
        self.output.merge(generated)

    def generate_model(self, node):
        generated = self.generate(node)
        generated.pop("enabled", None)
        generated.pop("type", None)

        return {**node.section_global_mapping.section, "mappings": generated}

    def generate(self, node):
        mapping: Section = node.section_mapping
        ret = {**mapping.section}

        if not isinstance(node, ModelDataType):
            if not deep_searchable_enabled(node):
                ret.setdefault("enabled", False)
                return ret

            if ret.get("enabled") is False:
                return ret

        if mapping.children:
            properties = ret.setdefault("properties", {})
            for k, v in mapping.children.items():
                v = self.generate(v)
                if k in properties:
                    deepmerge(properties[k], v)
                else:
                    properties[k] = v
        if mapping.item:
            v = self.generate(mapping.item)
            ret.pop("type", None)
            deepmerge(ret, v)
        if ret.get("enabled") is True:  # keep only enabled: False there
            ret.pop("enabled")
        return ret
