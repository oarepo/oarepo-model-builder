from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordServiceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_service"
    section = "service"
    template = "service"
