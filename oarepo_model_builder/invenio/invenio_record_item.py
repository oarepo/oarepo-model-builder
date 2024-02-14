from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordItemBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_item"
    section = "record-item"
    template = "record-item"
