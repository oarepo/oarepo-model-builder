from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordPIDProviderBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_pid_provider"
    section = "pid"
    template = "pid-provider"
