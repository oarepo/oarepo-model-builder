from pathlib import Path

from ..utils.verbose import log
from .json_base import JSONBaseBuilder
from .utils import ensure_parent_modules


class MappingBuilder(JSONBaseBuilder):
    TYPE = "mapping"
    output_file_type = "mapping"
    output_file_name = "mapping-file"
    parent_module_root_name = "mappings"

    def build_node(self, node):
        self.output.merge(node.mapping)
