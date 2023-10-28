from .invenio_record_marshmallow import InvenioRecordMarshmallowBuilder


class InvenioRecordUIMarshmallowBuilder(InvenioRecordMarshmallowBuilder):
    TYPE = "invenio_record_ui_schema"
    template = "marshmallow"
    extra_imports = []

    build_class_method = "ui_marshmallow_build_class"
