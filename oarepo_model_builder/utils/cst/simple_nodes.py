from .common import MergerBase, IdentityBaseMerger, PythonContext
from .mergers import expression_mergers, simple_line_mergers


class AssignMerger(MergerBase):
    def merge(self, context: PythonContext, existing_node, new_node):
        merged_value = self.check_and_merge(context, existing_node.value, new_node.value, expression_mergers)
        if merged_value:
            return existing_node.with_changes(
                value=merged_value
            )
        return existing_node

    def node_to_name(self, node):
        return tuple(sorted([x.target.value for x in node.targets]))

    def should_merge(self, context: PythonContext, existing_node, new_node):
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


class SimpleStringMerger(IdentityBaseMerger):
    pass


class NameMerger(IdentityBaseMerger):
    pass


class FunctionMerger(MergerBase):
    def merge(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def should_merge(self, context: PythonContext, existing_node, new_node):
        return existing_node.name.value == new_node.name.value


class SimpleStatementLineMerger(MergerBase):

    def should_merge(self, context: PythonContext, existing_node, new_node):
        assert len(existing_node.body) == 1
        assert len(new_node.body) == 1
        return self.get_node_merger(context, existing_node.body[0], new_node.body[0], simple_line_mergers)

    def merge(self, context: PythonContext, existing_node, new_node):
        try:
            context.push(existing_node, new_node)
            return existing_node.with_changes(
                body=[
                    self.check_and_merge(context, existing_node.body[0], new_node.body[0],
                                         simple_line_mergers) or existing_node.body[0]
                ]
            )
        finally:
            context.pop()
