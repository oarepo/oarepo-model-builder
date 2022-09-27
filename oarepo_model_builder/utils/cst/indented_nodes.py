from libcst import Assign, ClassDef, Import, ImportFrom, SimpleStatementLine

from .common import IdentityMerger, MergerBase, PythonContext, node_with_type
from .mergers import indented_block_mergers


class PriorityMergerMixin:
    def extract_body(self, node):
        raise NotImplementedError()

    def get_node_type(self, node_type_category, node):
        if isinstance(node, SimpleStatementLine):
            node = node.body[0]
        t = type(node)
        return node_type_category.get(t, "unknown")

    def _merge_children_with_priorities(
        self, context, existing_node, updated_node, mergers, node_type_category
    ):
        existing_list = self.extract_body(existing_node)
        new_list = self.extract_body(updated_node)

        ret = []
        existing_list = [
            node_with_type(e, self.get_node_type(node_type_category, e))
            for e in existing_list
        ]
        new_list = [
            node_with_type(e, self.get_node_type(node_type_category, e))
            for e in new_list
        ]

        last_type = None
        for existing in existing_list:
            merger = mergers.get(type(existing.node), IdentityMerger())
            if last_type is not None and last_type != existing.type:
                while new_list and new_list[0].type == last_type:
                    new_node = new_list.pop(0).node
                    new_merger = mergers.get(type(new_node), IdentityMerger())
                    ret.append(new_merger.merge(context, None, new_node))
            last_type = existing.type
            found = False
            for idx, new in enumerate(new_list):
                if new.type != existing.type:
                    break
                if isinstance(existing.node, type(new.node)):
                    if merger.identity(context, existing.node).deep_equals(
                        merger.identity(context, new.node)
                    ):
                        ret.append(merger.merge(context, existing.node, new.node))
                        del new_list[idx]
                        found = True
                        break
            if not found:
                ret.append(merger.merge(context, existing.node, None))

        for node in new_list:
            merger = mergers.get(type(node.node), IdentityMerger())
            ret.append(merger.merge(context, None, node.node))

        return self.finalize(existing_node, ret)

    def finalize(self, existing_node, body):
        raise NotImplementedError()


class ModuleMerger(PriorityMergerMixin, MergerBase):
    def identity(self, context, node):
        return node

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        return self._merge_children_with_priorities(
            context,
            existing_node,
            new_node,
            mergers=indented_block_mergers,
            node_type_category={
                Import: "import",
                ImportFrom: "import",
                ClassDef: "classdef",
                Assign: "assign",
            },
        )

    def extract_body(self, node):
        return node.body

    def finalize(self, existing_node, body):
        return existing_node.with_changes(body=body)


class ClassMerger(PriorityMergerMixin, MergerBase):
    def identity(self, context, node):
        return node.name

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        return self._merge_children_with_priorities(
            context,
            existing_node,
            new_node,
            mergers=indented_block_mergers,
            node_type_category={
                Import: "import",
                ImportFrom: "import",
                ClassDef: "classdef",
                Assign: "assign",
            },
        )

    def extract_body(self, node):
        return node.body.body

    def finalize(self, node, new_content):
        return node.with_changes(body=node.body.with_changes(body=new_content))
