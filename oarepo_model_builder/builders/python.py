from pathlib import Path

from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.builders.utils import ensure_parent_modules
from oarepo_model_builder.utils.jinja import package_name


class PythonBuilder(OutputBuilder):
    def module_to_path(self, module_name):
        mod = module_name.split(".")
        mod[-1] += ".py"
        return Path(*mod)

    def create_parent_modules(self, python_path: Path):
        ensure_parent_modules(
            self.builder, python_path, max_depth=len(python_path.parts)
        )

    def class_to_path(self, class_name):
        return self.module_to_path(package_name(class_name))

    def build_node(self, datatype):
        "intended to be overridden in children"
