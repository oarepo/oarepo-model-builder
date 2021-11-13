import os
from pathlib import Path

from deepdiff import DeepDiff

from .json_stack import JSONStack
from . import OutputBase
from ..schema import deepmerge

try:
    import json5
except ImportError:
    import json as json5


class JSONOutput(OutputBase):
    IGNORE_NODE = JSONStack.IGNORED_NODE
    IGNORE_SUBTREE = JSONStack.IGNORED_SUBTREE

    def begin(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    self.original_data = json5.load(f)  # noqa
            except ValueError:
                self.original_data = None
        else:
            self.original_data = None
        self.stack = JSONStack()

    def finish(self):
        data = self.stack.value
        if DeepDiff(data, self.original_data):
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, 'w') as f:
                json5.dump(data, f)

    def enter(self, key, el):
        if key:
            self.stack.push(key, el)

    def leave(self):
        if not self.stack.empty:
            self.stack.pop()

    def primitive(self, key, value):
        if key:
            self.stack.push(key, value)
            self.stack.pop()
