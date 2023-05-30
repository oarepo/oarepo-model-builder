from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record"
    section = "record"
    template = "record"
    record_section = "section_record"
    record_metadata_section = "section_record_metadata"
    pid_section = "section_pid"
    mapping_section = "section_mapping_settings"

    def finish(self, **extra_kwargs):
        super().finish(record=getattr(self.current_model, self.record_section).config,
                       record_metadata=getattr(self.current_model, self.record_metadata_section).config,
                       pid=getattr(self.current_model, self.pid_section).config,
                       mapping_settings=getattr(self.current_model, self.mapping_section).config,
                       **extra_kwargs)

