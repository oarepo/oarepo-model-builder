from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordBuilder(InvenioBaseClassPythonBuilder):
    class_config = 'record-class'
    template = 'record'
