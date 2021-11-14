import libcst as cst

from oarepo_model_builder.outputs import OutputBase


class PythonOutput(OutputBase):
    output_type = 'python'

    def begin(self):
        if self.path.exists():
            with self.path.open() as f:
                self.original_data = f.read()

                self.cst = cst.parse_module(self.original_data)
        else:
            self.original_data = None
            self.cst = cst.parse_module('')

    def finish(self):
        code = self.cst.code
        if code != self.original_data:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open(mode='w') as f:
                f.write(code)

    def get_class(self, name):
        ret = PythonClass(self, ((cst.ClassDef, name),))
        if not ret.exists:
            ret.create(name)
        return ret

    def create_cst(self, new_cst, path):
        self.cst = self.cst.visit(CreatingTransformer(path, new_cst))


class CreatingTransformer(cst.CSTTransformer):
    def __init__(self, path, new_cst):
        super().__init__()
        self.path = path
        self.new_cst = new_cst
        if path:
            raise Exception('Creating nested stuff not supported yet')

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        if not self.path:
            return updated_node.with_changes(
                body=[
                    *updated_node.body,
                    *self.new_cst
                ]
            )


class CSTPart:
    def __init__(self, output, path):
        self.output = output
        self.path = path

    @property
    def _cst(self):
        current = self.output.cst
        for p in self.path:
            for c in current.body:
                if isinstance(c, p[0]) and c.name.value == p[1]:
                    current = c
                    break
            else:
                return None
        return current

    @property
    def exists(self):
        return self._cst is not None

    def _create(self, expr):
        self.output.create_cst(
            cst.parse_module(expr, config=self.output.cst.config_for_parsing).body,
            self.path[:-1]
        )


class PythonClass(CSTPart):
    def __init__(self, output, path):
        super().__init__(output, path)

    def create(self, name=None):
        expr = f"""
class {name}:
    pass
        """
        return self._create(expr)
