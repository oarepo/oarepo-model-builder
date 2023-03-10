from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordUISerializerBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_ui_serializer"
    class_config = "record-ui-serializer-class"
    template = "record-ui-serializer"

    def finish(self, **extra_kwargs):

        ui_record_schema_class = (
            self.current_model.get("ui", {})
            .get("marshmallow", {})
            .get("schema-class", self.current_model.record_schema_class)
        )

        return super().finish(
            ui_record_schema_class=ui_record_schema_class, **extra_kwargs
        )
