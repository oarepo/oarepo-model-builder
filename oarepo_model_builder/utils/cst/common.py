from collections import namedtuple

from libcst import SimpleStatementLine

from .mergers import general_mergers


class PythonContext:
    def __init__(self, cst):
        self.cst = cst
        self.stack = []

    def to_source_code(self, node):
        return self.cst.code_for_node(node)

    def push(self, node):
        self.stack.push(node)

    def pop(self, node):
        self.stack.pop(node)


def real_node(node):
    if isinstance(node, SimpleStatementLine):
        return node.body[0]
    return node


def real_with_changes(node, **kwargs):
    if isinstance(node, SimpleStatementLine):
        return node.with_changes(
            body=[
                node.body[0].with_changes(**kwargs)
            ]
        )
    else:
        return node.with_changes(**kwargs)


node_with_type = namedtuple('node_with_type', 'node, type')


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
        if type(real_node(new_node)) is not type(real_node(existing_node)):
            return None
        merger = mergers.get(type(real_node(existing_node)), IdentityMerger())
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
            return context.to_source_code(real_node(existing_node)).strip() == context.to_source_code(real_node(new_node)).strip()
        except AttributeError:
            print('')
            raise


class IdentityMerger(IdentityBaseMerger):
    def merge(self, context: PythonContext, existing_node, new_node):
        return existing_node

    def should_merge(self, context: PythonContext, existing_node, new_node):
        print(
            f'Warning: using naive merger for {type(real_node(existing_node))}'
            f'>>>\n{context.to_source_code(existing_node).strip()}\n<<<')
        return super().should_merge(context, existing_node, new_node)


def merge(context: PythonContext, existing_node, new_node, mergers=None):
    if not mergers:
        mergers = general_mergers

    real_existing = real_node(existing_node)
    real_new = real_node(new_node)

    if type(real_existing) is not type(real_new):
        return None
    merger = mergers.get(type(real_existing), IdentityMerger())
    if merger.should_merge(context, existing_node, new_node):
        return merger.merge(context, existing_node, new_node)
    return None
