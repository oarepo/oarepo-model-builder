from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordUISerializerBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_ui_serializer"
    class_config = "record-ui-serializer-class"
    template = "record-ui-serializer"
