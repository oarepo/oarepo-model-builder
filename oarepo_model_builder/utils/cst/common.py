from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from logging import getLogger
from typing import List, Set, Union

from libcst import Arg, CSTNode, Element, Module

from .mergers import module_mergers

logger = getLogger("oarepo_model_builder.cst")


class OperationPerformed(Enum):
    ADD = 1
    CHANGE = 2
    REMOVAL = 3


class ConflictResolution(Enum):
    KEEP_PREVIOUS = 1
    KEEP_NEW = 2
    KEEP_MERGED = 3
    REMOVE = 4
    NEW_AS_TODO = 5


class ConflictResolver:
    def resolve_conflict(
        self, context, existing_node, new_node, merged_node  # NOSONAR
    ) -> ConflictResolution:
        return ConflictResolution.KEEP_PREVIOUS


@dataclass
class PythonContextItem:
    existing_node: CSTNode
    new_node: CSTNode
    operations: Set[OperationPerformed] = field(default_factory=set, init=False)
    new_as_comment: bool = field(default=False, init=False)


@dataclass
class PythonContext:
    cst: Module
    stack: List[PythonContextItem] = field(default_factory=list, init=False)

    REMOVED = object()

    def to_source_code(self, node):
        if not node:
            return ""
        return self.cst.code_for_node(node)

    def push(self, existing_node: CSTNode, new_node: CSTNode):
        self.stack.append(
            PythonContextItem(existing_node=existing_node, new_node=new_node)
        )

    def pop(self):
        self.stack.pop()

    @property
    def top(self):
        return self.stack[-1]

    def decide(
        self,
        existing_node: Union[CSTNode, None],
        new_node: Union[CSTNode, None],
        merged_node: Union[CSTNode, None],
    ) -> Union[CSTNode, object]:
        logger.debug(
            "\nDecide called with operations %s on node %s %s",
            self.top.operations,
            type(existing_node or new_node).__name__,
            id(existing_node),
        )
        logger.debug("Existing: %s", self.to_source_code(existing_node))
        logger.debug("New     : %s", self.to_source_code(new_node))
        logger.debug("Merged  : %s", self.to_source_code(merged_node))

        top = self.top
        decision = None
        if existing_node is self.top.existing_node:
            # processing existing node. If there was any decision in children, do not decide here
            if top.operations:
                decision = ConflictResolution.KEEP_MERGED
            if len(self.stack) > 1:
                top = self.stack[-2]
        if _get_source_code(self, existing_node) == _get_source_code(self, new_node):
            decision = ConflictResolution.KEEP_PREVIOUS
        if decision is None:
            if existing_node:
                decision = ConflictResolution.KEEP_PREVIOUS
            else:
                decision = ConflictResolution.KEEP_NEW

        logger.debug("")
        if decision == ConflictResolution.KEEP_PREVIOUS:
            return existing_node
        elif decision == ConflictResolution.KEEP_NEW:
            top.operations.add(OperationPerformed.ADD)
            return new_node
        elif decision == ConflictResolution.KEEP_MERGED:
            top.operations.add(OperationPerformed.CHANGE)
            return merged_node
        elif decision == ConflictResolution.REMOVE:
            top.operations.add(OperationPerformed.REMOVAL)
            return self.REMOVED
        elif decision == ConflictResolution.NEW_AS_TODO:  # NOSONAR
            top.new_as_comment = True
            return existing_node
        raise RuntimeError("Unknown decision")


node_with_type = namedtuple("node_with_type", "node, type")


class MergerBase:
    def merge(self, context: PythonContext, existing_node, new_node):
        try:
            context.push(existing_node, new_node)
            if existing_node and new_node and isinstance(new_node, type(existing_node)):
                ret = self.merge_internal(context, existing_node, new_node)
            else:
                ret = existing_node or new_node
            return context.decide(existing_node, new_node, ret)
        finally:
            context.pop()

    def identity(self, context, node):
        print(
            f"Warning: using naive merger for {type(node)}"
            f">>>\n{context.to_source_code(node).strip()}\n<<<"
        )
        return node

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        raise NotImplementedError()


class IdentityBaseMerger(MergerBase):
    def merge_internal(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def identity(self, context, node):
        return node


class IdentityMerger(IdentityBaseMerger):
    def merge_internal(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def identity(self, context, node):
        print(
            f"Warning: using naive merger for {type(node)}"
            f">>>\n{context.to_source_code(node).strip()}\n<<<"
        )
        return node


def merge(context: PythonContext, existing_node, new_node, mergers=None):
    if not mergers:
        mergers = module_mergers

    merger = mergers.get(type(existing_node or new_node), IdentityMerger())
    return merger.merge(context, existing_node, new_node)


def _get_source_code(context, node):
    if isinstance(node, (Arg, Element)):
        node = node.value
    return context.to_source_code(node)
