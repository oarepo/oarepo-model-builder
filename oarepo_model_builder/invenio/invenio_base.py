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

        output.merge(
            self.template,
            HyphenMunch(settings=self.settings, python=self.settings.python, **extra_kwargs)
        )
