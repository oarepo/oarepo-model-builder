from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordResourceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_resource_config"
    section = "resource-config"
    template = "resource-config"

    def finish(self, **extra_kwargs):
        profile = self.current_model.profile
        super().finish(profile=profile, **extra_kwargs)