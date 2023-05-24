import copy
import json

from deepdiff import DeepDiff

from ..utils.deepmerge import deepmerge
from ..utils.verbose import log
from . import OutputBase
from .json_stack import JSONStack

try:
    import json5
except ImportError:
    import json as json5


class JSONOutput(OutputBase):
    IGNORE_NODE = JSONStack.IGNORED_NODE
    IGNORE_SUBTREE = JSONStack.IGNORED_SUBTREE
    TYPE = "json"

    def begin(self):
        try:
            with self.builder.filesystem.open(self.path) as f:
                self.original_data = json5.load(f)  # noqa
                self.data = copy.deepcopy(self.original_data)
        except FileNotFoundError:
            self.original_data = None
            self.data = {}
        except ValueError:
            self.original_data = None
            self.data = {}

    @property
    def created(self):
        return self.original_data is None

    def force_clean_output(self):
        self.original_data = None

    def finish(self):
        # create differing but non-empty files
        if DeepDiff(self.data, self.original_data) and (
            self.data or self.original_data
        ):
            self.builder.filesystem.mkdir(self.path.parent)
            log(2, "Saving %s", self.path)
            with self.builder.filesystem.open(self.path, mode="w") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

    def merge(self, value):
        self.data = deepmerge(value, self.data)

    @property
    def modified(self):
        return DeepDiff(self.data, self.original_data) and (
            self.data or self.original_data
        )
