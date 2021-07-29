from typing import List

from ..builder import BaseBuilder


class JSONBuilder(BaseBuilder):
    """Hierarchic json builder."""
    IGNORED_SUBTREE = object()
    IGNORED_NODE = object()

    def __init__(self):
        self.stack: List = [{}]

    def push(self, el, path):
        top = self.stack[-1]
        if top is self.IGNORED_SUBTREE:
            self.stack.append(self.IGNORED_SUBTREE)
        elif el is self.IGNORED_SUBTREE or el is self.IGNORED_NODE:
            self.stack.append(el)
        else:
            if top is self.IGNORED_NODE:
                for t in reversed(self.stack[:-1]):
                    if t is not self.IGNORED_NODE:
                        top = t
                        break

            if isinstance(top, dict):
                top[path[-1]] = el
            elif isinstance(top, (list, tuple)):
                top.append(el)
            else:
                raise NotImplemented(f'Set for datatype {type(top)} is not implemented')
            self.stack.append(el)

    def pop(self):
        self.stack.pop()
