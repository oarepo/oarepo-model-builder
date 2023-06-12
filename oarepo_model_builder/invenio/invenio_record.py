from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record"
    section = "record"
    template = "record"
