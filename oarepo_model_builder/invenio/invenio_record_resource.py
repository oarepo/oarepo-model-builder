from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordResourceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_resource"
    section = "resource"
    template = "resource"
