from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioCliBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_cli"
    class_config = "cli-function"
    template = "cli"
