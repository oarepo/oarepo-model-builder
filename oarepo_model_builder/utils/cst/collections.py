from oarepo_model_builder.utils.cst import PythonContext
from oarepo_model_builder.utils.cst.common import IdentityMerger, MergerBase
from oarepo_model_builder.utils.cst.mergers import expression_mergers


class ElementMerger(MergerBase):
    """list element"""

    def identity(self, context: PythonContext, node):
        node_value = node.value
        merger = expression_mergers.get(type(node_value), IdentityMerger())
        return merger.identity(context, node_value)

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        existing_value = existing_node.value
        new_value = new_node.value

        merger = expression_mergers.get(type(existing_value), IdentityMerger())
        return existing_node.with_changes(value=merger.merge(context, existing_value, new_value))


class ListMerger(MergerBase):
    def identity(self, context: PythonContext, node):
        return node

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        return existing_node.with_changes(
            elements=merge_lists_remove_duplicates(
                context, existing_node.elements, new_node.elements, expression_mergers
            )
        )


class DictMerger(MergerBase):
    def identity(self, context: PythonContext, node):
        return node

    def get_key(self, context, el):
        if hasattr(el, 'key') and el.key:
            return el.key.value
        # TODO: StarredDictElement might contain trailing comma, should remove it
        return context.to_source_code(el)

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        ret = []
        mergers = expression_mergers
        existing_elements = {self.get_key(context, el): el for el in existing_node.elements}
        new_elements = {self.get_key(context, el): el for el in new_node.elements}
        for k, el in existing_elements.items():
            merger = mergers.get(type(el), IdentityMerger())
            if k not in new_elements:
                ret.append(merger.merge(context, el, None))
            else:
                new_element = new_elements.pop(k)
                ret.append(merger.merge(context, el, new_element))

        for k, el in new_elements.items():
            merger = mergers.get(type(el), IdentityMerger())
            merged = merger.merge(context, None, el)
            ret.append(merged)
        return existing_node.with_changes(elements=[x for x in ret if x is not context.REMOVED])


def merge_lists_remove_duplicates(context: PythonContext, existing_list, new_list, mergers):
    ret = []
    new_list = [*new_list]

    for e in existing_list:
        merger = mergers.get(type(e), IdentityMerger())
        e_identity = merger.identity(context, e)

        for idx, n in enumerate(new_list):
            if not isinstance(n, type(e)):
                continue
            n_identity = merger.identity(context, n)
            if e_identity.deep_equals(n_identity):
                ret.append(merger.merge(context, e, n))
                del new_list[idx]
                break
        else:
            ret.append(merger.merge(context, e, None))

    for n in new_list:
        merger = mergers.get(type(n), IdentityMerger())
        ret.append(merger.merge(context, None, n))

    return [x for x in ret if x is not context.REMOVED]
