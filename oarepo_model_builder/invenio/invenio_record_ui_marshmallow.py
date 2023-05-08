from oarepo_model_builder.datatypes import Import

from .invenio_record_marshmallow import InvenioRecordMarshmallowBuilder


class InvenioRecordUIMarshmallowBuilder(InvenioRecordMarshmallowBuilder):
    TYPE = "invenio_record_ui_schema"
    class_config = "record-ui-schema-class"
    template = "marshmallow"
    extra_imports = [Import("oarepo_runtime.ui.marshmallow.InvenioUISchema")]

    build_class_method = "ui_marshmallow_build_class"
