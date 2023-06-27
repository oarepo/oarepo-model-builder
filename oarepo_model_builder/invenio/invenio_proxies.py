from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioProxiesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_proxies"
    section = "proxy"
    template = "proxies"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
