import json

from deepdiff import DeepDiff

from . import OutputBase
from .json_stack import JSONStack

try:
    import json5
except ImportError:
    import json as json5


class JSONOutput(OutputBase):
    IGNORE_NODE = JSONStack.IGNORED_NODE
    IGNORE_SUBTREE = JSONStack.IGNORED_SUBTREE

    def begin(self):
        if self.path.exists():
            try:
                with self.path.open() as f:
                    self.original_data = json5.load(f)  # noqa
            except ValueError:
                self.original_data = None
        else:
            self.original_data = None
        self.stack = JSONStack()

    def finish(self):
        data = self.stack.value
        if DeepDiff(data, self.original_data):
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open(mode='w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

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
