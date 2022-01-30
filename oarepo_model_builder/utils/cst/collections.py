from oarepo_model_builder.utils.cst import PythonContext
from oarepo_model_builder.utils.cst.common import MergerBase, merge
from oarepo_model_builder.utils.cst.mergers import expression_mergers
from oarepo_model_builder.utils.cst.utils import merge_lists_remove_duplicates


class ElementMerger(MergerBase):
    """list element"""

    def should_merge(self, context: PythonContext, existing_node, new_node):
        return self.get_node_merger(
            context, existing_node.value, new_node.value, expression_mergers
        )

    def merge(self, context: PythonContext, existing_node, new_node):
        return existing_node.with_changes(
            value=self.check_and_merge(
                context, existing_node.value, new_node.value, expression_mergers
            )
            or existing_node.value
        )


class ListMerger(MergerBase):
    def should_merge(self, context: PythonContext, existing_node, new_node):
        return True

    def merge(self, context: PythonContext, existing_node, new_node):
        return existing_node.with_changes(
            elements=merge_lists_remove_duplicates(
                existing_node.elements, new_node.elements, context, expression_mergers
            )
        )


class DictMerger(MergerBase):
    def should_merge(self, context: PythonContext, existing_node, new_node):
        return True

    def merge(self, context: PythonContext, existing_node, new_node):
        ret = []
        existing_elements = {el.key.value: el for el in existing_node.elements}
        new_elements = {el.key.value: el for el in new_node.elements}
        for k, el in existing_elements.items():
            if k not in new_elements:
                ret.append(el)
            else:
                ret.append(
                    el.with_changes(
                        value=merge(
                            context,
                            el.value,
                            new_elements.pop(k).value,
                            expression_mergers,
                        )
                        or el.value
                    )
                )
        for k, el in new_elements.items():
            ret.append(el)
        return existing_node.with_changes(elements=ret)
