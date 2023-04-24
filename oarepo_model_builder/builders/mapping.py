from pathlib import Path

from ..utils.verbose import log
from ..utils.deepmerge import deepmerge
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


def deep_searchable_enabled(dt):
    mapping = dt.section_mapping
    if mapping.section.get("facets", {}).get("searchable", None) is False:
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
        generated = self.generate(node, Section({}, node.children, None))
        return {**node.section_mapping.section, "mappings": generated}

    def generate(self, node, mapping: Section = None):
        if not mapping:
            mapping: Section = node.section_mapping

        ret = {**mapping.section}

        if not deep_searchable_enabled(node):
            ret.setdefault("enabled", False)
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
            deepmerge(ret, v)
        return ret
