from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    class_config = 'record-service-config-class'
    template = 'record-service-config'
