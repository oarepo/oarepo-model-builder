from .invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


class InvenioRecordUISchemaBuilder(InvenioRecordSchemaBuilder):
    TYPE = "invenio_record_ui_schema"
    class_config = "record-ui-schema-class"
    template = "record-schema"
    OAREPO_MARSHMALLOW_PROPERTY = "ui_marshmallow"
    extra_imports = [
        HyphenMunch({"import-path": "oarepo_runtime.ui.marshmallow.InvenioUISchema"})
    ]
