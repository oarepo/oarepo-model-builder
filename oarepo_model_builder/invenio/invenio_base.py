from pathlib import Path

from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.datatypes.datatypes import MergedAttrDict
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.dict import dict_get
from oarepo_model_builder.utils.python_name import module_to_path


class InvenioBaseClassPythonBuilder(PythonBuilder):
    section: str
    template: str
    parent_modules = True
    skip_if_not_generating = True

    @property
    def generate(self):
        if hasattr(self, "section") and dict_get(
            self.current_model.definition, [self.section, "skip"], False
        ):
            return False

        if (
            self.skip_if_not_generating
            and hasattr(self, "section")
            and not dict_get(
                self.current_model.definition, [self.section, "generate"], False
            )
        ):
            return False
        return True

    @property
    def vars(self):
        section = getattr(
            self.current_model,
            f"section_mb_{self.TYPE.replace('-', '_')}",
        )

        vars = MergedAttrDict(section.config, self.current_model.definition)
        return vars

    def finish(self, **extra_kwargs):
        super().finish()
        if not self.generate:
            return

        module = self._get_output_module()
        python_path = Path(module_to_path(module) + ".py")

        self.process_template(
            python_path,
            self.template,
            current_module=module,
            vars=self.vars,
            **extra_kwargs,
        )

    def _get_output_module(self):
        module = self.current_model.definition[self.section]["module"]
        return module

    def process_template(self, python_path: Path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)
        context = dict(
            settings=self.settings,
            current_model=self.current_model,
            schema=self.current_model.schema.schema,
            **extra_kwargs,
        )
        output.merge(template, context)
