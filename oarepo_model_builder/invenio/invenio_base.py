from pathlib import Path

from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.datatypes.datatypes import MergedAttrDict
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.jinja import package_name
from oarepo_model_builder.utils.python_name import module_to_path


class InvenioBaseClassPythonBuilder(PythonBuilder):
    section: str
    template: str
    # section = None
    # template = None
    parent_modules = True

    def finish(self, **extra_kwargs):
        super().finish()
        module = self.current_model.definition[self.section]['module']
        python_path = Path(module_to_path(module) + ".py")

        section = getattr(
            self.current_model,
            f"section_mb_{self.TYPE.replace('-', '_')}",
        )
        merged = MergedAttrDict(section.config, self.current_model.definition)
        self.process_template(
            python_path,
            self.template,
            current_module=module,
            vars=merged,
            **extra_kwargs,
        )

    def process_template(self, python_path: Path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)
        context = dict(
            settings=self.settings, current_model=self.current_model, **extra_kwargs
        )
        output.merge(template, context)
