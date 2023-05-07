from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordMetadataBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_metadata"
    section = "record-metadata"
    template = "record-metadata"
