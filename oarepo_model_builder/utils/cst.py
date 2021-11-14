from libcst import CSTTransformer, ClassDef, FunctionDef, Module, SimpleStatementLine, Import, ImportFrom


class MergingTransformer(CSTTransformer):
    def __init__(self, new_cst):
        super().__init__()
        self.new_cst = new_cst
        self.stack = []
        self._push(new_cst.body)

    def _push(self, new_members):
        self.stack.append((new_members, {}))

    def _pop(self):
        return self.stack.pop()

    def _set(self, key, value):
        self.stack[-1][1][key] = value

    def visit_ClassDef(self, node: ClassDef):
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

    def leave_Module(self, original_node: Module, updated_node: Module):
        parts_to_add = self.leave_class_module()

        new_imports = self._extract_imports(self.stack[0][0])
        existing_imports = self._extract_imports(original_node.body)

        # extract imports that are not yet present
        extra_imports = []
        for ni in new_imports:
            for ei in existing_imports:
                if ei.deep_equals(ni):
                    break
            else:
                extra_imports.append(ni)

        self._pop()

        # and merge
        return updated_node.with_changes(
            body=[
                *extra_imports,
                *updated_node.body,
                *parts_to_add
            ]
        )

    def _extract_imports(self, lines):
        imports = []
        for l in lines:
            if isinstance(l, SimpleStatementLine):
                for ml in l.children:
                    if isinstance(ml, (Import, ImportFrom)):
                        imports.append(l)
                        break
        return imports

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
