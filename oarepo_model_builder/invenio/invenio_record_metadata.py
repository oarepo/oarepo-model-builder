from .invenio_base import InvenioBaseClassPythonBuilder

class InvenioRecordMetadataBuilder(InvenioBaseClassPythonBuilder):
    class_config = 'record-metadata-class'
    template = 'record-metadata'
