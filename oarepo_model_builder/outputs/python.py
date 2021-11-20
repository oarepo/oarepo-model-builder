import pkgutil
from typing import Optional

import libcst as cst
import pkg_resources
from jinja2 import Environment, FunctionLoader

from oarepo_model_builder.invenio.template_registry import templates
from oarepo_model_builder.outputs import OutputBase
from oarepo_model_builder.utils.cst import MergingTransformer
from oarepo_model_builder.utils.verbose import log


class PythonOutput(OutputBase):
    output_type = 'python'

    def begin(self):
        if self.path.exists():
            with self.builder.open(self.path) as f:
                self.original_data = f.read()

                self.cst = cst.parse_module(self.original_data)
        else:
            self.original_data = None
            self.cst = cst.parse_module('')

    def finish(self):
        code = self.cst.code
        if code != self.original_data:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            log(2, 'Saving %s', self.path)
            with self.builder.open(self.path, mode='w') as f:
                f.write(code)

    def merge(self, template_name, context):
        # template is a loadable resource
        env = Environment(
            loader=FunctionLoader(lambda tn: getattr(templates, tn)),
            autoescape=False
        )
        rendered = env.get_template(template_name).render(context)
        rendered_cst = cst.parse_module(rendered, config=self.cst.config_for_parsing)
        self.cst = self.cst.visit(MergingTransformer(rendered_cst))



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
