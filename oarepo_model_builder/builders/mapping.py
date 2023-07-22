from ..datatypes import ModelDataType, Section
from ..utils.deepmerge import deepmerge
from ..utils.dict import dict_get
from .json_base import JSONBaseBuilder


def deep_searchable_enabled(dt):
    mapping = dt.section_mapping
    facets = dt.section_facets
    if (
        mapping.config.get("enabled", None) is False
        or facets.config.get("searchable") is False
    ):
        return False
    if mapping.item:
        return deep_searchable_enabled(mapping.item)
    if not mapping.children:
        return True
    for c in mapping.children.values():
        if deep_searchable_enabled(c):
            return True
    return False


class MappingBuilder(JSONBaseBuilder):
    TYPE = "mapping"
    output_file_type = "mapping"
    output_file_name = ["mapping", "file"]
    skip = ["mapping", "skip"]
    parent_module_root_name = "mappings"
    create_parent_packages = True

    def build_node(self, node):
        skip = dict_get(self.current_model.definition, ["mapping", "skip"], False)
        if skip:
            return
        generated = self.generate_model(node)
        generated.pop("enabled", None)
        template = dict_get(self.current_model.definition, ["mapping", "template"], {})
        if template:
            self.output.merge(template)
        self.output.merge(generated)

    def generate_model(self, node):
        generated = self.generate(node)
        generated.pop("enabled", None)
        generated.pop("type", None)
        node.section_global_mapping.config.pop("properties", None)

        return {**node.section_global_mapping.config, "mappings": generated}

    def generate(self, node, parent_enabled=True):
        mapping: Section = node.section_mapping
        facets: Section = node.section_facets
        ret = {**mapping.config}
        enabled_property = (
            "enabled" if mapping.config.get("type") in ("object", "nested") else "index"
        )

        searchable = facets.config.get("searchable")
        if searchable is not None:
            ret.setdefault(enabled_property, searchable)

        this_node_enabled = True
        if not isinstance(node, ModelDataType):
            if not deep_searchable_enabled(node):
                ret.setdefault(enabled_property, False)
                return ret

            if not parent_enabled:
                ret.setdefault(enabled_property, False)

            if ret.get(enabled_property) is False:
                return ret
        else:
            this_node_enabled = deep_searchable_enabled(node)

        if mapping.children:
            properties = ret.setdefault("properties", {})
            for k, v in mapping.children.items():
                v = self.generate(v, this_node_enabled)
                if k in properties:
                    deepmerge(properties[k], v)
                else:
                    properties[k] = v
        if mapping.item:
            v = self.generate(mapping.item, this_node_enabled)
            ret.pop("type", None)
            deepmerge(ret, v)
        if ret.get(enabled_property) is True:  # keep only enabled: False there
            ret.pop(enabled_property)
        return ret
