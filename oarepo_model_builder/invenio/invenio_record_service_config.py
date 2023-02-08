from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch

from ..utils.jinja import base_name
from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_service_config"
    class_config = "record-service-config-class"
    template = "record-service-config"

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
