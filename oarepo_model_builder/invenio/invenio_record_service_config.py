from .invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
from ..utils.jinja import base_name


class InvenioRecordServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_service_config"
    class_config = "record-service-config-class"
    template = "record-service-config"

    def process_template(self, python_path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)

        expandable_fields_context = []
        expandable_fields_classes = set()
        expandable_fields = getattr(self.current_model, "expandable_fields", [])
        for expandable_field in expandable_fields:
            service_alias = getattr(
                expandable_field,
                "service_alias",
                base_name(expandable_field.field_name) + "_service",
            )
            expandable_field_class = getattr(
                expandable_field,
                "expandable_field_class",
                "oarepo_records_resources.services.expandable_fields.ReferencedRecordExpandableField",
            )
            expandable_fields_context.append(
                {
                    "field_name": expandable_field.field_name,
                    "referenced_keys": expandable_field.referenced_keys,
                    "service": expandable_field.service,
                    "pid_field": getattr(expandable_field, "pid_field", None),
                    "service_alias": service_alias,
                    "expandable_field_class": expandable_field_class,
                }
            )
            expandable_fields_classes.add(expandable_field_class)

        context = HyphenMunch(
            settings=self.settings,
            current_model=self.current_model,
            expandable_fields_context=expandable_fields_context,
            expandable_fields_classes=expandable_fields_classes,
            **extra_kwargs
        )
        template = self.call_components(
            "invenio_before_python_template", template, context=context
        )
        output.merge(template, context)
