import sys
from typing import Mapping

import libcst as cst
from jinja2 import Environment, FunctionLoader, Undefined, pass_context

from oarepo_model_builder.outputs import OutputBase
from oarepo_model_builder.templates import templates
from oarepo_model_builder.utils.cst import PythonContext, merge
from oarepo_model_builder.utils.jinja import (
    base_name,
    class_header,
    generate_import,
    generate_list,
    in_different_package,
    package_name,
)
from oarepo_model_builder.utils.verbose import log


class PythonOutput(OutputBase):
    TYPE = "python"
    cst = None
    original_data = None

    def begin(self):
        try:
            with self.builder.filesystem.open(self.path) as f:
                self.original_data = f.read()

                self.cst = cst.parse_module(self.original_data)
        except FileNotFoundError:
            self.original_data = None
            self.cst = cst.parse_module("")

    @property
    def created(self):
        return self.original_data is None

    def finish(self):
        code = self.cst.code
        if code != self.original_data:
            self.builder.filesystem.mkdir(self.path.parent)
            log(2, "Saving %s", self.path)
            with self.builder.filesystem.open(self.path, mode="w") as f:
                f.write(code)
            if self.builder.schema.settings["python"]["use-isort"]:
                import isort

                config = isort.settings.Config(verbose=False, quiet=True)
                isort.file(self.path, config=config)
            if self.builder.schema.settings["python"]["use-black"]:
                import subprocess

                subprocess.call(["black", "-q", "--preview", str(self.path)])
            if self.builder.schema.settings["python"]["use-autoflake"]:
                import subprocess

                subprocess.call(
                    [
                        "autoflake",
                        "--in-place",
                        "--remove-all-unused-imports",
                        str(self.path),
                    ]
                )

    def merge(self, template_name, context, filters=None):
        # template is a loadable resource
        env = Environment(
            loader=FunctionLoader(
                lambda tn: templates.get_template(tn, context["settings"])
            ),
            autoescape=False,
            undefined=StrictUndefined,
        )
        self.register_default_filters(env)
        for filter_name, filter_func in (filters or {}).items():
            env.filters[filter_name] = filter_func

        try:
            context = {
                **context,
                **{k.replace("-", "_"): v for k, v in list(context.items())},
            }
            rendered = env.get_template(template_name).render(make_attrdict(context))
        except Exception as exc:
            raise RuntimeError(
                f"Error rendering template {template_name}: {str(exc)}"
            ) from exc
        try:
            rendered_cst = cst.parse_module(
                rendered, config=self.cst.config_for_parsing
            )
        except:
            print(rendered, file=sys.stderr)
            raise

        try:
            self.cst = merge(
                PythonContext(rendered_cst),
                self.cst,
                rendered_cst,
            )
        except:
            print(rendered)
            print("====")
            print(self.original_data)
            raise

    @staticmethod
    def register_default_filters(env):
        env.filters["generate_import"] = generate_import
        env.filters["generate_list"] = generate_list
        env.filters["class_header"] = class_header
        env.filters["package_name"] = package_name
        env.filters["base_name"] = pass_context(lambda context, value: base_name(value))
        env.tests["in_different_package"] = pass_context(
            lambda context, value: in_different_package(
                context["current_module"], value
            )
        )


class AttrDict(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(f"No key {item}") from e

    def __getitem__(self, item):
        if super().__contains__(item):
            ret = super().__getitem__(item)
        else:
            ret = super().__getitem__(item.replace("_", "-"))

        if isinstance(ret, Mapping) and not isinstance(ret, AttrDict):
            return AttrDict(ret)
        return ret

    def items(self):
        return [(k, self[k]) for k in self]

    def values(self):
        return [self[k] for k in self]

    def __contains__(self, item):
        return super().__contains__(item) or super().__contains__(
            item.replace("_", "-")
        )


class StrictUndefined(Undefined):
    def __str__(self):
        self._fail_with_undefined_error()


def make_attrdict(d):
    d = AttrDict(d)
    return {k: d[k] for k in d}
