from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioAPIViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_api_views"
    section = "api-blueprint"
    template = "api-views"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
