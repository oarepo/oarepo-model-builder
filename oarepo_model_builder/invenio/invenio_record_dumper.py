from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordDumperBuilder(InvenioBaseClassPythonBuilder):
    output_builder_type = 'invenio_record_dumper'
    class_config = 'record-dumper-class'
    template = 'record-dumper'
