from __future__ import annotations

import functools
import inspect
import sys
from typing import TYPE_CHECKING, List

from oarepo_model_builder.utils.json_pathlib import JSONPaths
from oarepo_model_builder.utils.verbose import log

if TYPE_CHECKING:
    from oarepo_model_builder.builder import ModelBuilder
    from oarepo_model_builder.datatypes.datatypes import DataType


class OutputBuilder:
    TYPE = None

    def __init__(self, builder: ModelBuilder):
        self.builder = builder
        self.datatype_stack = None
        self.silent_exceptions = False

    def begin(self, current_model: DataType, schema):
        self.schema = schema
        self.current_model = current_model
        self.settings = schema["settings"]
        log.enter(2, "Creating %s", self.TYPE)
        self.silent_exceptions = False
        self.datatype_stack = []

    def finish(self):
        log.leave()

    def build(self, current_model, schema):
        self.begin(current_model, schema)
        self.process_node(self.current_model)
        self.finish()

    def process_node(self, node: DataType):
        try:
            self.datatype_stack.append(node)
            self.build_node(node)
            self.datatype_stack.pop()
        except Exception as e:
            if not self.silent_exceptions:
                self.silent_exceptions = True
                print(
                    f"Error on handling path {self.datatype_stack[-1].path}: {e}",
                    file=sys.stderr,
                )
            raise

    def build_children(self):
        parent_node = self.datatype_stack[-1]
        for child in parent_node.children.items():
            self.process_node(child)

    def process_node(self, datatype: DataType):
        pass


TEMPLATES = {
    "setup_py": "templates/setup.py.jinja2",
}

__all__ = [
    "OutputBuilder",
    "TEMPLATES",
]
