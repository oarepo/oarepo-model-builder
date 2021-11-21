from .invenio_base import InvenioBaseClassPythonBuilder

class InvenioRecordPermissionsBuilder(InvenioBaseClassPythonBuilder):
    class_config = 'record-permissions-class'
    template = 'record-permissions'
