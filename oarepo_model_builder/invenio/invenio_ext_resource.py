from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioExtResourceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_ext_resource"
    section = "ext"
    template = "ext-resource"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
