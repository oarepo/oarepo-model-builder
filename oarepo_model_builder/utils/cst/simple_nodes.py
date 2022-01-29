from .common import MergerBase, real_node, real_with_changes, IdentityBaseMerger
from .mergers import expression_mergers
from .utils import merge_lists_remove_duplicates


class AssignMerger(MergerBase):
    def merge(self, cst, existing_node, new_node):
        real_existing = real_node(existing_node)
        real_new = real_node(new_node)
        merged_value = self.check_and_merge(cst, real_existing.value, real_new.value, expression_mergers)
        if merged_value:
            return real_with_changes(
                existing_node,
                value=merged_value
            )
        return existing_node

    def node_to_name(self, node):
        return tuple(sorted([x.target.value for x in real_node(node).targets]))

    def should_merge(self, cst, existing_node, new_node):
        return self.node_to_name(existing_node) == self.node_to_name(new_node)


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


class FunctionMerger(MergerBase):
    def merge(self, cst, existing_node, new_node):
        return existing_node

    def should_merge(self, cst, existing_node, new_node):
        return existing_node.name.value == new_node.name.value


class ElementMerger(MergerBase):
    """ list element """

    def should_merge(self, cst, existing_node, new_node):
        return self.get_node_merger(cst, existing_node.value, new_node.value, expression_mergers)

    def merge(self, cst, existing_node, new_node):
        return real_with_changes(
            existing_node,
            value=self.check_and_merge(cst, existing_node.value, new_node.value,
                                       expression_mergers) or existing_node.value
        )


class ListMerger(MergerBase):
    def should_merge(self, cst, existing_node, new_node):
        return True

    def merge(self, cst, existing_node, new_node):
        return real_with_changes(existing_node, elements=merge_lists_remove_duplicates(
            real_node(existing_node).elements, real_node(new_node).elements,
            cst, expression_mergers
        ))
