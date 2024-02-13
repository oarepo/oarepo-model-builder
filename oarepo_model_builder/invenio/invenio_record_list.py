from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordListBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_list"
    section = "record-list"
    template = "record-list"
