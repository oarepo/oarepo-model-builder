from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioExtBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_ext"
    section = "ext"
    template = "ext"
