from .invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


class InvenioRecordServiceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_service"
    class_config = "record-service-class"
    template = "record-service"

    def process_template(self, python_path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)
        context = HyphenMunch(
            settings=self.settings,
            current_model=self.current_model,
            schema=self.schema,
            **extra_kwargs
        )
        template = self.call_components(
            "invenio_before_python_template", template, context=context
        )
        output.merge(template, context)