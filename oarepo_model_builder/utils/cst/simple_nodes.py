import logging

from libcst import Assign, Integer, Name

from .common import IdentityBaseMerger, IdentityMerger, MergerBase, PythonContext
from .mergers import expression_mergers, simple_line_mergers

log = logging.getLogger("oarepo_model_builder.cst")


class AssignMerger(MergerBase):
    def merge_internal(self, context: PythonContext, existing_node, new_node):
        merger = expression_mergers.get(type(existing_node.value or new_node.value), IdentityMerger())
        merged_value = merger.merge(context, existing_node.value, new_node.value)
        return existing_node.with_changes(value=merged_value)

    def identity(self, context, node):
        return Assign(targets=node.targets, value=Integer(value="1"))


class ImportMerger(IdentityBaseMerger):
    pass


class ImportFromMerger(IdentityBaseMerger):
    pass


class ExprMerger(IdentityBaseMerger):
    pass


class PassMerger(IdentityBaseMerger):
    pass


class IntegerMerger(IdentityBaseMerger):
    pass


class SimpleStringMerger(IdentityBaseMerger):
    pass


class NameMerger(IdentityBaseMerger):
    pass


class StarredElementMerger(IdentityBaseMerger):
    pass


class FunctionMerger(MergerBase):
    def merge_internal(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def identity(self, context, node):
        return node.name


class SimpleStatementLineMerger(MergerBase):
    def identity(self, context, node):
        assert len(node.body) == 1
        body = node.body[0]
        if type(body) in simple_line_mergers:
            return simple_line_mergers[type(body)].identity(context, body)
        log.error("Could not find node %s in simple_line_mergers", type(node))
        return node.body[0]

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        existing_body = existing_node.body[0] if existing_node else None
        new_body = new_node.body[0] if new_node else None
        merger = simple_line_mergers.get(type(existing_body or new_body), IdentityMerger())
        return existing_node.with_changes(body=[merger.merge(context, existing_body, new_body)])
