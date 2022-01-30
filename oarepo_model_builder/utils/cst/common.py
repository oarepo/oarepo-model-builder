from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Set

from libcst import CSTNode, Module

from .mergers import module_mergers

from logging import getLogger


logger = getLogger('oarepo_model_builder.cst')


class OperationPerformed(Enum):
    ADD = 1
    CHANGE = 2
    REMOVAL = 3


class Decision(Enum):
    KEEP_PREVIOUS = 1
    KEEP_NEW = 2
    KEEP_MERGED = 3
    REMOVE = 4
    NEW_AS_TODO = 5


@dataclass
class PythonContextItem:
    existing_node: CSTNode
    new_node: CSTNode
    operations: Set[OperationPerformed] = field(default_factory=set, init=False)
    new_as_comment: bool = field(default=False, init=False)


@dataclass
class PythonContext:
    cst: Module
    decider: Callable[["PythonContext", CSTNode, CSTNode, CSTNode, str], Decision] = None
    stack: List[PythonContextItem] = field(default_factory=list, init=False)

    REMOVED = object()

    def to_source_code(self, node):
        if not node:
            return ''
        return self.cst.code_for_node(node)

    def push(self, existing_node: CSTNode, new_node: CSTNode):
        self.stack.append(PythonContextItem(existing_node=existing_node, new_node=new_node))

    def pop(self):
        self.stack.pop()

    @property
    def top(self):
        return self.stack[-1]

    def decide(
            self,
            existing_node: CSTNode | None,
            new_node: CSTNode | None,
            merged_node: CSTNode | None,
            explanation: str = None,
    ) -> CSTNode | object:

        logger.debug(
            f'\nDecide called with operations {self.top.operations} on node {type(existing_node or new_node).__name__} {id(existing_node)}')
        logger.debug('Existing: ', self.to_source_code(existing_node))
        logger.debug('New     : ', self.to_source_code(new_node))
        logger.debug('Merged  : ', self.to_source_code(merged_node))

        top = self.top
        if existing_node is self.top.existing_node:
            # processing existing node. If there was any decision in children, do not decide here
            decision = Decision.KEEP_MERGED
            if len(self.stack) > 1:
                top = self.stack[-2]
        else:
            if existing_node:
                decision = Decision.KEEP_PREVIOUS
            else:
                decision = Decision.KEEP_NEW

            if self.decider:
                decision = self.decider(self, existing_node, new_node, merged_node, explanation)
        logger.debug('---> ', decision)
        logger.debug('')
        match decision:
            case Decision.KEEP_PREVIOUS:
                return existing_node
            case Decision.KEEP_NEW:
                top.operations.add(OperationPerformed.ADD)
                return new_node
            case Decision.KEEP_MERGED:
                top.operations.add(OperationPerformed.CHANGE)
                return merged_node
            case Decision.REMOVE:
                top.operations.add(OperationPerformed.REMOVAL)
                return self.REMOVED
            case Decision.NEW_AS_TODO:
                top.new_as_comment = True
                return existing_node
        raise Exception('Unknown decision')


node_with_type = namedtuple("node_with_type", "node, type")


class MergerBase:
    def merge(self, context: PythonContext, existing_node, new_node):
        try:
            context.push(existing_node, new_node)
            if existing_node and new_node:
                ret = self.merge_internal(context, existing_node, new_node)
            else:
                ret = existing_node or new_node
            return context.decide(existing_node, new_node, ret)
        finally:
            context.pop()

    def merge_internal(self, context: PythonContext, existing_node, new_node):
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
    def merge_internal(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def should_merge(self, context: PythonContext, existing_node, new_node):
        try:
            return context.to_source_code(existing_node).strip() == context.to_source_code(new_node).strip()
        except AttributeError:
            print("")
            raise


class IdentityMerger(IdentityBaseMerger):
    def merge_internal(self, context: PythonContext, existing_node, new_node):
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
