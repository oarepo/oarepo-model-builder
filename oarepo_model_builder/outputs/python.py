import sys
import libcst as cst
from jinja2 import Environment, FunctionLoader

from oarepo_model_builder.templates import templates
from oarepo_model_builder.outputs import OutputBase
from oarepo_model_builder.utils.cst import MergingTransformer
from oarepo_model_builder.utils.verbose import log


class PythonOutput(OutputBase):
    TYPE = 'python'

    def begin(self):
        try:
            with self.builder.open(self.path) as f:
                self.original_data = f.read()

                self.cst = cst.parse_module(self.original_data)
        except FileNotFoundError:
            self.original_data = None
            self.cst = cst.parse_module('')

    @property
    def created(self):
        return self.original_data is None

    def finish(self):
        code = self.cst.code
        if code != self.original_data:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            log(2, 'Saving %s', self.path)
            with self.builder.open(self.path, mode='w') as f:
                f.write(code)
            if self.builder.schema.settings.python.use_isort:
                import isort
                config = isort.settings.Config(verbose=False, quiet=True)
                isort.file(self.path, config=config)
            if self.builder.schema.settings.python.use_black:
                import subprocess
                subprocess.call([
                    'black',
                    '-q',
                    '--experimental-string-processing',
                    str(self.path)
                ])

    def merge(self, template_name, context, filters=None):
        # template is a loadable resource
        env = Environment(
            loader=FunctionLoader(lambda tn: templates.get_template(tn, context['settings'])),
            autoescape=False,
        )
        self.register_default_filters(env)
        for filter_name, filter_func in (filters or {}).items():
            env.filters[filter_name] = filter_func

        rendered = env.get_template(template_name).render(context)
        try:
            rendered_cst = cst.parse_module(rendered, config=self.cst.config_for_parsing)
        except:
            print(rendered, file=sys.stderr)
            raise
        self.cst = self.cst.visit(MergingTransformer(rendered_cst))

    def register_default_filters(self, env):
        env.filters['package_name'] = lambda value: (value.rsplit('.', maxsplit=1)[0])
        env.filters['base_name'] = lambda value: (value.rsplit('.', maxsplit=1)[1])


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
