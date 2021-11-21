from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    output_builder_type = 'invenio_record_service_config'
    class_config = 'record-service-config-class'
    template = 'record-service-config'
