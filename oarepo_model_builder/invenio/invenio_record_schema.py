from .invenio_base import InvenioBaseClassPythonBuilder

class InvenioRecordSchemaBuilder(InvenioBaseClassPythonBuilder):
    class_config = 'record-schema-class'
    template = 'record-schema'
