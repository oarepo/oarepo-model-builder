from collections import defaultdict

from libcst import CSTTransformer, ClassDef, FunctionDef, Module, SimpleStatementLine, Import, ImportFrom, Assign, Name, \
    AssignTarget, List, Expr, CSTVisitor, IndentedBlock, Element

from typing import Dict, Type


class StackItem:
    def __init__(self, existing_node, new_node):
        self.existing_node = existing_node
        self.existing_members = defaultdict(list)
        self.new_members = defaultdict(list)

    def add_existing(self, item_type, item):
        self.existing_members[item_type].append(item)

    def add_new(self, item_type, item):
        self.new_members[item_type].append(item)


def merge(existing_cst, new_cst, top_cst=None):
    return existing_cst.visit(MergingTransformer(top_cst or new_cst, new_cst, mergers))


class MergingTransformer(CSTTransformer):
    def __init__(self, top_cst, new_cst, mergers, finalizer=None):
        super().__init__()
        self.top_cst = top_cst
        self.new_cst = new_cst
        self.mergers = mergers
        self.finalizer = finalizer

    def on_visit(self, node):  # do not process children
        return False

    def on_leave(self, original_node, updated_node):
        existing = self.extract_body(updated_node)
        new = self.extract_body(self.new_cst)

        ret = []
        for node_type, existing_nodes in existing.items():
            if node_type not in new:
                ret.extend(existing_nodes)
                continue
            new_nodes = new.pop(node_type)

            merger = self.mergers.get(node_type, IdentityMerger())

            for existing_node in existing_nodes:
                for idx, new_node in enumerate(new_nodes):
                    if merger.should_merge(self.top_cst, existing_node, new_node):
                        ret.append(merger.merge(self.top_cst, existing_node, new_node))
                        del new_nodes[idx]
                        break
                else:
                    ret.append(existing_node)

            ret.extend(new_nodes)
        for node_type, new_nodes in new.items():
            ret.extend(new_nodes)
        if self.finalizer:
            return self.finalizer(updated_node, ret)
        else:
            return updated_node.with_changes(
                body=ret
            )

    def extract_body(self, node):
        ret = defaultdict(list)
        if hasattr(node, 'body'):
            body = node.body
        elif isinstance(node, List):
            body = node.elements
        else:
            raise Exception(f'Do not know how to get body from {node}')
        if isinstance(body, IndentedBlock):
            body = body.body
        for n in body:
            if isinstance(n, SimpleStatementLine):
                node_type = type(n.body[0])
            else:
                node_type = type(n)
            ret[node_type].append(n)
        return ret


class MergerBase:
    def merge(self, cst, existing_node, new_node):
        raise NotImplementedError()

    def should_merge(self, cst, existing_node, new_node):
        return False

    def real_node(self, node):
        if isinstance(node, SimpleStatementLine):
            return node.body[0]
        return node

    def real_with_changes(self, node, **kwargs):
        if isinstance(node, SimpleStatementLine):
            return node.with_changes(
                body=[
                    node.body[0].with_changes(**kwargs)
                ]
            )
        else:
            return node.with_changes(**kwargs)


class IdentityBaseMerger(MergerBase):
    def merge(self, cst, existing_node, new_node):
        return existing_node

    def should_merge(self, cst, existing_node, new_node):
        return cst.code_for_node(existing_node).strip() == cst.code_for_node(new_node).strip()


class IdentityMerger(IdentityBaseMerger):
    def merge(self, cst, existing_node, new_node):
        return existing_node

    def should_merge(self, cst, existing_node, new_node):
        print(
            f'Warning: using naive merger for {type(self.real_node(existing_node))}'
            f'>>>\n{cst.code_for_node(existing_node).strip()}\n<<<')
        return super().should_merge(cst, existing_node, new_node)


class ClassMerger(MergerBase):
    def merge(self, cst, existing_node, new_node):
        return existing_node.visit(MergingTransformer(cst, new_node, mergers, finalizer=self.finalize))

    def finalize(self, node, new_content):
        return node.with_changes(
            body=node.body.with_changes(body=new_content)
        )

    def should_merge(self, cst, existing_node, new_node):
        return existing_node.name.value == new_node.name.value


class AssignMerger(MergerBase):
    def merge(self, cst, existing_node, new_node):
        # TODO: merge arrays, dictionaries etc
        real_existing = self.real_node(existing_node)
        real_new = self.real_node(new_node)
        if isinstance(real_existing.value, List) or isinstance(real_new.value, List):
            return self.real_with_changes(existing_node, value=self.merge_lists(
                cst, real_existing.value, real_new.value
            ))
        return existing_node

    def merge_lists(self, cst, existing_list, new_list):
        return existing_list.visit(MergingTransformer(cst, new_list, list_mergers, finalizer=self.finalize_list))

    def finalize_list(self, node, new_content):
        return node.with_changes(elements=new_content)

    def node_to_name(self, node):
        return tuple(sorted([x.target.value for x in self.real_node(node).targets]))

    def should_merge(self, cst, existing_node, new_node):
        return self.node_to_name(existing_node) == self.node_to_name(new_node)


class ImportMerger(IdentityBaseMerger):
    pass


class ImportFromMerger(IdentityBaseMerger):
    pass


class ExprMerger(IdentityBaseMerger):
    pass


class FunctionMerger(MergerBase):
    def merge(self, cst, existing_node, new_node):
        return existing_node

    def should_merge(self, cst, existing_node, new_node):
        return existing_node.name.value == new_node.name.value


class ElementMerger(MergerBase):
    def merge(self, cst, existing_node, new_node):
        return existing_node

    def should_merge(self, cst, existing_node, new_node):
        return cst.code_for_node(existing_node.value).strip() == cst.code_for_node(new_node.value).strip()


mergers = {
    ClassDef: ClassMerger(),
    Assign: AssignMerger(),
    Import: ImportMerger(),
    ImportFrom: ImportFromMerger(),
    Expr: ExprMerger(),
    FunctionDef: FunctionMerger()
}

list_mergers = {
    Element: ElementMerger()
}


class MergingTransformerOld(CSTTransformer):

    def __init__(self, new_cst):
        super().__init__()
        self.new_cst = new_cst
        self.stack = []

    def visit_Module(self, node: "Module"):
        self._push(node, self.new_cst)

    def leave_Module(self, original_node: Module, updated_node: Module):
        item = self._pop()

        parts_to_add = self._get_new_parts(item.existing_members, item.new_members)

        self._pop()

        # and merge
        return updated_node.with_changes(
            body=[
                *parts_to_add['import'],
                *updated_node.body,
                *parts_to_add['class'],
                *parts_to_add['assign']
            ]
        )

    def visit_Import(self, node: Import):
        self.top.add_existing('import', node)
        return False

    def visit_ImportFrom(self, node: "ImportFrom"):
        self.top.add_existing('import', node)
        return False

    def _push(self, existing_node, new_node):
        self.stack.append(StackItem(existing_node, new_node))

    def _pop(self):
        return self.stack.pop()

    def _get_new_parts(self, existing_parts, new_parts):
        keys = set(existing_parts.keys()) | set(new_parts.keys())
        to_add = defaultdict(list)

        for k in keys:
            existing_list = existing_parts.get(k, [])
            new_list = new_parts.get(k, [])

            for new_item in new_list:
                new_item_name = self._node_name(new_item)
                for existing_item in existing_list:
                    if self._node_name(existing_item) == new_item_name:
                        break
                else:
                    to_add[k].append(new_item)
        return to_add

    def _node_name(self, node):
        if isinstance(node, SimpleStatementLine):
            body = node.body
            if not len(body):
                raise NotImplementedError(f'No body in SimpleStatementLine {node}')
            name_element = body[0]
        else:
            name_element = node

        if isinstance(name_element, Assign):
            lhs = name_element.children[0]
            if not isinstance(lhs, AssignTarget):
                raise NotImplementedError(f'Getting name of node type {type(lhs)} not implemented yet')
            return lhs.target.value
        elif isinstance(name_element, (Import, ImportFrom)):
            return 'Import:' + self.new_cst.code_for_node(name_element).strip()
        elif isinstance(name_element, (Expr,)):
            return 'Expr:' + self.new_cst.code_for_node(name_element).strip()
        elif isinstance(name_element, (FunctionDef,)):
            return 'Function:' + name_element.name.value
        else:
            raise NotImplementedError(f'Getting name of node type {type(name_element)} not implemented yet')

    @property
    def top(self):
        return self.stack[-1]

    def visit_ClassDef(self, node: ClassDef):
        self.top.add_existing()
        self._set(node.name.value, node)
        for part in self.stack[-1][0]:
            if hasattr(part, 'name'):
                if part.name.value == node.name.value:
                    if hasattr(part, 'body'):
                        self._push(part.body.body)
                        break
        else:
            self._push([])

    def visit_FunctionDef(self, node: FunctionDef):
        # do not visit the children of the function as we do not modify
        # an already written function code
        self._set(node.name.value, node)
        return False

    def leave_ClassDef(
            self, original_node: ClassDef, updated_node: ClassDef
    ):
        parts_to_add = self.leave_class_module()
        self._pop()

        if parts_to_add:
            # and merge them with the original content
            return updated_node.with_changes(
                body=updated_node.body.with_changes(
                    body=[
                        *updated_node.body.body,
                        *parts_to_add
                    ]
                )
            )
        return updated_node

    def visit_Assign(self, node):
        assign_name = self._node_name(node)
        stack_top = self.stack[-1][0]
        for el in stack_top:
            el_name = self._node_name(el)
            if el_name == assign_name and isinstance(node.value, List):
                self._push(remove_simple_line(el))
                return node
        self._push(None)
        return False

    def leave_Assign(self, original_node, updated_node):
        self._pop()
        return updated_node

    def leave_List(self, original_node, updated_node):
        stack_top = self.stack[-1][0]
        if not isinstance(stack_top, Assign):
            return False
        # TODO: merge
        node_elements = list(updated_node.elements)
        for el in stack_top.value.elements:
            for ne in updated_node.elements:
                if ne.value.deep_equals(el.value):
                    break
            else:
                node_elements.append(el)
        return updated_node.with_changes(
            elements=node_elements
        )

    def _merge_assign_value(self, target_node, source_node):
        return target_node

    def _merge_imports(self, original_node):
        new_imports = self._extract_imports(self.stack[0][0])
        existing_imports = self._extract_imports(original_node.body)
        return self._merge_nodes(existing_imports, new_imports)

    def _merge_assigns(self, original_node):
        new_assigns = self._extract_assigns(self.stack[0][0])
        existing_assigns = self._extract_assigns(original_node.body)
        return self._merge_nodes(existing_assigns, new_assigns)

    def _merge_nodes(self, existing_nodes, new_nodes):
        # extract nodes that are not yet present
        extra_nodes = []
        for ni in new_nodes:
            for ei in existing_nodes:
                if self._node_name(ei) == self._node_name(ni):
                    break
            else:
                extra_nodes.append(ni)
        return extra_nodes

    def _extract_imports(self, lines):
        return self._extract_top_level(lines, (Import, ImportFrom))

    def _extract_assigns(self, lines):
        return self._extract_top_level(lines, Assign)

    def _extract_top_level(self, lines, classes=()):
        extracted = []
        for l in lines:
            if isinstance(l, SimpleStatementLine):
                for ml in l.children:
                    if isinstance(ml, classes):
                        extracted.append(l)
                        break
        return extracted

    def leave_class_module(self):
        new_parts = self.stack[-1][0]
        existing_parts = self.stack[-1][1]

        # look for the parts in the new parts that are not in the existing parts
        parts_to_add = []
        for part in new_parts:
            if hasattr(part, 'name'):
                if part.name.value not in existing_parts:
                    parts_to_add.append(part)
        return parts_to_add


def remove_simple_line(node):
    if isinstance(node, SimpleStatementLine):
        return node.body[0]
    return node
