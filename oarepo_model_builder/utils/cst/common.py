from collections import namedtuple
from dataclasses import dataclass
from typing import List

from libcst import CSTNode

from .mergers import module_mergers

DecisionRequired = namedtuple("DecisionRequired", "existing_node, new_node, explanation")


@dataclass
class PythonContextItem:
    existing_node: CSTNode
    new_node: CSTNode
    decisions = List[DecisionRequired]


class PythonContext:
    stack: List[PythonContextItem]

    def __init__(self, cst):
        self.cst = cst
        self.stack = []

    def to_source_code(self, node):
        return self.cst.code_for_node(node)

    def push(self, existing_node: CSTNode, new_node: CSTNode):
        self.stack.append(PythonContextItem(existing_node=existing_node, new_node=new_node))

    def pop(self):
        self.stack.pop()

    @property
    def top(self):
        return self.stack[-1]

    def add_decision_required(self, existing_node: CSTNode, new_node: CSTNode, explanation: str):
        self.top.decisions.append(DecisionRequired(existing_node, new_node, explanation))


node_with_type = namedtuple("node_with_type", "node, type")


class MergerBase:
    def merge(self, context: PythonContext, existing_node, new_node):
        raise NotImplementedError()

    def should_merge(self, context: PythonContext, existing_node, new_node):
        return False

    def get_node_merger(self, context: PythonContext, existing_node, new_node, mergers):
        """
        Returns a merger for the existing node only if it is capable of merging
        the new_node (that is, if the should_merge on the merger returns True)

        Otherwise, None is returned
        """
        if type(new_node) is not type(existing_node):
            return None
        merger = mergers.get(type(existing_node), IdentityMerger())
        if merger.should_merge(context, existing_node, new_node):
            return merger
        return None

    def check_and_merge(self, context: PythonContext, existing_node, new_node, mergers):
        merger = self.get_node_merger(context, existing_node, new_node, mergers)
        if merger:
            return merger.merge(context, existing_node, new_node)
        return None


class IdentityBaseMerger(MergerBase):
    def merge(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def should_merge(self, context: PythonContext, existing_node, new_node):
        try:
            return (
                context.to_source_code(existing_node).strip()
                == context.to_source_code(new_node).strip()
            )
        except AttributeError:
            print("")
            raise


class IdentityMerger(IdentityBaseMerger):
    def merge(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def should_merge(self, context: PythonContext, existing_node, new_node):
        print(
            f"Warning: using naive merger for {type(existing_node)}"
            f">>>\n{context.to_source_code(existing_node).strip()}\n<<<"
        )
        return super().should_merge(context, existing_node, new_node)


def merge(context: PythonContext, existing_node, new_node, mergers=None):
    if not mergers:
        mergers = module_mergers

    if type(existing_node) is not type(new_node):
        return None
    merger = mergers.get(type(existing_node), IdentityMerger())
    if merger.should_merge(context, existing_node, new_node):
        return merger.merge(context, existing_node, new_node)
    return None
