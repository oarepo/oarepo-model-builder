from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioAPIViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_api_views"
    section = "api-blueprint"
    template = "api-views"
