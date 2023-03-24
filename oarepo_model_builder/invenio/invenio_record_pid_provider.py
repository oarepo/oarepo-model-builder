from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordPIDProviderBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_pid_provider"
    class_config = "record-pid-provider-class"
    template = "record-pid-provider"