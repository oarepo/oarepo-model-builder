from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


class InvenioBaseClassPythonBuilder(PythonBuilder):
    class_config = None
    template = None

    def finish(self, **extra_kwargs):
        python_path = self.class_to_path(self.settings.python[self.class_config])
        self.create_parent_modules(python_path)

        output: PythonOutput = self.builder.get_output(
            'python',
            python_path
        )

        context = HyphenMunch(settings=self.settings, python=self.settings.python, **extra_kwargs)
        template = self.call_components('invenio_before_python_template', self.template, context=context)
        output.merge(
            template,
            context
        )
