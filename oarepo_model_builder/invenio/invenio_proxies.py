from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioProxiesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_proxies"
    section = "proxy"
    template = "proxies"
