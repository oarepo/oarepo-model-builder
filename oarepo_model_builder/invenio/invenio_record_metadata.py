from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordMetadataBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_metadata"
    section = "record-metadata"
    template = "record-metadata"
    record_section = "section_record"
    record_metadata_section = "section_record_metadata"


    def finish(self, **extra_kwargs):
        super().finish(record=getattr(self.current_model, self.record_section).config,
                       record_metadata=getattr(self.current_model, self.record_metadata_section).config,
                       **extra_kwargs)
