from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordResourceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_resource_config"
    section = "resource-config"
    template = "resource-config"
