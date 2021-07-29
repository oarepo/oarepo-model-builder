from typing import List

from ..builder import BaseBuilder


class JSONBuilder(BaseBuilder):
    """Hierarchic json builder."""
    IGNORED = object()

    def __init__(self):
        self.stack: List = [{}]

    def push(self, el, path):
        top = self.stack[-1]
        if el is not self.IGNORED and top is not self.IGNORED:
            if isinstance(top, dict):
                top[path[-1]] = el
            elif isinstance(top, (list, tuple)):
                top.append(el)
            else:
                raise NotImplemented(f'Set for datatype {type(top)} is not implemented')
            self.stack.append(el)
        else:
            self.stack.append(self.IGNORED)

    def pop(self):
        self.stack.pop()
