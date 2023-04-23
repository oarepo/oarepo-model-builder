from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_views"
    class_config = "create-blueprint-from-app"
    template = "views"
