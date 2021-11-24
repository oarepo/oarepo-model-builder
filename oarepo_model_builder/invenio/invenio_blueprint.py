from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioBlueprintBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_blueprint'
    class_config = 'register-blueprint-function'
    template = 'blueprint'
