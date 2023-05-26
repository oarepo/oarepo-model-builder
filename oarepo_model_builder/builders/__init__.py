from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from oarepo_model_builder.utils.verbose import log

if TYPE_CHECKING:
    from oarepo_model_builder.builder import ModelBuilder
    from oarepo_model_builder.datatypes.datatypes import DataType


class OutputBuilder:
    TYPE = None

    def __init__(self, builder: ModelBuilder):
        self.builder = builder
        self.silent_exceptions = False

    def begin(self, current_model: DataType, schema):
        self.schema = schema
        self.current_model = current_model
        self.settings = schema["settings"]
        log.enter(2, "Creating %s", self.TYPE)
        self.silent_exceptions = False

    def finish(self):
        log.leave()

    def build(self, current_model, schema):
        self.begin(current_model, schema)
        self._build_node_internal(self.current_model)
        self.finish()

    def _build_node_internal(self, node):
        try:
            self.build_node(node)
        except Exception as e:
            if not self.silent_exceptions:
                self.silent_exceptions = True
                print(
                    f"Error on handling path {node.path}: {e}",
                    file=sys.stderr,
                )
            raise

    def build_children(self, parent_node):
        for child in parent_node.children.items():
            self._build_node_internal(child)

    def build_node(self, datatype: DataType):
        "Intended to be overriden in children"


TEMPLATES = {
    "setup_py": "templates/setup.py.jinja2",
}

__all__ = [
    "OutputBuilder",
    "TEMPLATES",
]
