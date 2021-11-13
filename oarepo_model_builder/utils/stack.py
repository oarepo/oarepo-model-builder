from functools import cached_property
from deepdiff import DeepDiff


class ModelBuilderStackEntry:
    def __init__(self, key=None, el=None):
        self.key = key
        self.el = el

    def __getitem__(self, item):
        return self.el[item]

    def __eq__(self, other):
        return self.key == other.key and not DeepDiff(self.key, other.key)

    def __str__(self):
        return f'{self.key} - {self.el}'


class ModelBuilderStack:
    DICT = 'dict'
    LIST = 'list'
    PRIMITIVE = 'primitive'

    def __init__(self, schema):
        self.schema = schema
        self.stack = [ModelBuilderStackEntry(None, schema.schema)]

    def __getitem__(self, item):
        return self.stack[item]

    def push(self, key, el):
        self._clear_path()
        self.stack.append(ModelBuilderStackEntry(key, el))

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
        t = self.top
        if isinstance(t.el, dict):
            return self.DICT
        if isinstance(t.el, list):
            return self.LIST
        return self.PRIMITIVE

    @cached_property
    def path(self):
        return '/' + '/'.join(x.key for x in self.stack if x.key)

    def _clear_path(self):
        if "path" in self.__dict__:
            del self.__dict__["path"]

    def process(self, on_enter, on_leave, on_primitive):
        from oarepo_model_builder.builders import ReplaceElement

        top_type = self.top_type
        if top_type == self.PRIMITIVE:
            return on_primitive(self)
        elif top_type == self.LIST:
            res = on_enter(self)
            if isinstance(res, ReplaceElement):
                return res
            items = [*self.top.el]
            idx = -1
            while items:
                idx += 1
                l = items.pop(0)
                self.push(idx, l)
                ret = self.process(on_enter, on_leave, on_primitive)
                self.pop()
                if isinstance(ret, ReplaceElement):
                    items = [*ret.data] + items
            on_leave(self)
        elif top_type == self.DICT:
            res = on_enter(self)
            if isinstance(res, ReplaceElement):
                return res
            items = [*self.top.el.items()]
            while items:
                k, v = items.pop(0)
                self.push(k, v)
                ret = self.process(on_enter, on_leave, on_primitive)
                self.pop()
                if isinstance(ret, ReplaceElement):
                    items = [*ret.data.items()] + items
            on_leave(self)
