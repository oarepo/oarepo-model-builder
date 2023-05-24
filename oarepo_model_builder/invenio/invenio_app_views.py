from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioAPPViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_app_views"
    section = "app-blueprint"
    template = "app-views"
