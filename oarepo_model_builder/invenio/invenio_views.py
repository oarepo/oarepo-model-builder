from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioAPIViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_api_views"
    section = "api-blueprint"
    template = "api-views"


class InvenioUIViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_ui_views"
    section = "ui-blueprint"
    template = "ui-views"
