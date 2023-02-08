from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
from oarepo_model_builder.utils.jinja import package_name


class InvenioBaseClassPythonBuilder(PythonBuilder):
    class_config = None
    template = None
    parent_modules = True

    def finish(self, **extra_kwargs):
        super().finish()
        python_path = self.class_to_path(self.current_model[self.class_config])
        self.process_template(
            python_path,
            self.template,
            current_package_name=package_name(self.current_model[self.class_config]),
            **extra_kwargs,
        )

    def process_template(self, python_path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)
        context = HyphenMunch(
            settings=self.settings, current_model=self.current_model, **extra_kwargs
        )
        template = self.call_components(
            "invenio_before_python_template", template, context=context
        )
        output.merge(template, context)
