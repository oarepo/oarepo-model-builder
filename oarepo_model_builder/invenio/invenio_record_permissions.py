from .invenio_base import InvenioBaseClassPythonBuilder

class InvenioRecordPermissionsBuilder(InvenioBaseClassPythonBuilder):
    output_builder_type = 'invenio_record_permissions'
    class_config = 'record-permissions-class'
    template = 'record-permissions'
