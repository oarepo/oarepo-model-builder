from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.datatypes.datatypes import MergedAttrDict
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.jinja import package_name


class InvenioBaseClassPythonBuilder(PythonBuilder):
    class_config = None
    template = None
    parent_modules = True

    def finish(self, **extra_kwargs):
        super().finish()
        python_path = self.class_to_path(
            self.current_model.definition[self.class_config]
        )
        section = getattr(
            self.current_model,
            f"section_mb_{self.TYPE.replace('-', '_')}",
        )
        merged = MergedAttrDict(section.config, self.current_model.definition)
        self.process_template(
            python_path,
            self.template,
            current_package_name=package_name(
                self.current_model.definition[self.class_config]
            ),
            vars=merged,
            **extra_kwargs,
        )

    def process_template(self, python_path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)
        context = dict(
            settings=self.settings, current_model=self.current_model, **extra_kwargs
        )
        output.merge(template, context)
