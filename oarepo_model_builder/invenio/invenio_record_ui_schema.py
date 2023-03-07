from .invenio_record_schema import InvenioRecordSchemaBuilder


class InvenioRecordUISchemaBuilder(InvenioRecordSchemaBuilder):
    TYPE = "invenio_record_ui_schema"
    class_config = "record-ui-schema-class"
    template = "record-schema"
    OAREPO_MARSHMALLOW_PROPERTY = "ui_marshmallow"
