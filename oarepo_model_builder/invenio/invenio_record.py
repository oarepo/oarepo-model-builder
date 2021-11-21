from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordBuilder(InvenioBaseClassPythonBuilder):
    output_builder_type = 'invenio_record'
    class_config = 'record-class'
    template = 'record'
