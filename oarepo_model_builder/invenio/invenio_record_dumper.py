from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordDumperBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_dumper"
    section = "record-dumper"
    template = "record-dumper"
