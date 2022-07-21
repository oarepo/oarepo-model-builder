from .invenio_base import InvenioBaseClassPythonBuilder
from ..builders import process


class InvenioRecordBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record"
    class_config = "record-class"
    template = "record"

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.relations = []

    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        self.build_children()
        data = self.stack.top.data
        if isinstance(data, dict) and 'invenio:relation' in data:
            self.relations.append(data['invenio:relation'])

    def process_template(self, python_path, template, **extra_kwargs):
        return super().process_template(python_path, template, **{
            **extra_kwargs,
            'invenio_relations': self.relations
        })
