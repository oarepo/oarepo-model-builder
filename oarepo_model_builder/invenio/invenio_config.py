from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_config"
    section = "config"
    template = "config"
