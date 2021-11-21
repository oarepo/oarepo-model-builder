from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordDumperBuilder(InvenioBaseClassPythonBuilder):
    class_config = 'record-dumper-class'
    template = 'record-dumper'
