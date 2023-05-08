from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordUISerializerBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_ui_serializer"
    section = "json-serializer"
    template = "ui-serializer"
