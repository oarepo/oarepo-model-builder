from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioAPPViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_app_views"
    section = "app-blueprint"
    template = "app-views"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
