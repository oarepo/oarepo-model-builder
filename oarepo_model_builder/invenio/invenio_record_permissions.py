from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordPermissionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_permissions"
    section = "permissions"
    template = "permissions"
