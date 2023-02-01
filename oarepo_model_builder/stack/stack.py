import json
from functools import cached_property

from deepdiff import DeepDiff

from .schema import Ref, SchemaPathValidator, model_paths


class ReplaceElement(Exception):
    def __init__(self, data):
        super().__init__()
        self.data = data


class RemoveElement(ReplaceElement):
    def __init__(self):
        super().__init__(None)


class ModelBuilderStackEntry:
    key: str
    schema: SchemaPathValidator

    def __init__(self, key: str, data, schema: SchemaPathValidator):
        self.key = key
        self.data = data
        self.schema = schema

    def __getitem__(self, item):
        return self.data[item]

    def __eq__(self, other):
        return self.key == other.key and not DeepDiff(self.key, other.key)

    def __str__(self):
        return f"{self.key} - {self.data}"

    @property
    def schema_valid(self):
        return self.schema.valid

    @property
    def schema_element_type(self):
        if self.schema_valid and isinstance(self.schema, Ref):
            return self.schema.element_type
        return None

    @property
    def json_schema_type(self):
        return self.data.get("type", None)


class ModelBuilderStack:
    DICT = "dict"
    LIST = "list"
    PRIMITIVE = "primitive"
    SKIP = "skip"

    def __init__(self):
        self.stack = []

    def __getitem__(self, item):
        return self.stack[item]

    def push(self, key, el):
        self._clear_path()
        if not self.stack:
            entry = ModelBuilderStackEntry(key, el, model_paths)
        else:
            try:
                entry = ModelBuilderStackEntry(key, el, self.top.schema.get(key))
            except Exception as e:
                print(self.top.schema.get(key))
        self.stack.append(entry)

    def pop(self):
        self._clear_path()
        self.stack.pop()

    @property
    def top(self):
        return self.stack[-1]

    @property
    def level(self):
        return len(self.stack)

    @property
    def top_type(self):
        if isinstance(self.top.data, dict):
            return self.DICT
        elif isinstance(self.top.data, list):
            return self.LIST
        else:
            return self.PRIMITIVE

    @cached_property
    def path(self):
        return "/" + "/".join(str(x.key) for x in self.stack if x.key)

    def _clear_path(self):
        if "path" in self.__dict__:
            del self.__dict__["path"]

    @property
    def schema_valid(self):
        if not self.stack:
            return False
        return self.top.schema_valid

    def clone(self):
        ret = type(self)()
        ret.stack.extend(self.stack)
        return ret

    @property
    def fingerprint(self):
        return json.dumps(
            self.stack[-1].data, sort_keys=True, default=lambda x: repr(x)
        ).encode("utf-8")
