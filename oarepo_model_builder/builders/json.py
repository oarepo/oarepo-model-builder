from typing import List

from oarepo_model_builder.builders.element import ElementBuilder


class JSONBuilder(ElementBuilder):
    """Hierarchic json builder."""
    IGNORED_SUBTREE = object()
    IGNORED_NODE = object()

    def __init__(self):
        self.stack: List = [{}]

    def should_ignore(self, element):
        return element is self.IGNORED_SUBTREE or element is self.IGNORED_NODE

    def push(self, el, path):
        top = self.stack[-1]
        if top is self.IGNORED_SUBTREE:
            self.stack.append(self.IGNORED_SUBTREE)
        elif self.should_ignore(el):
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
