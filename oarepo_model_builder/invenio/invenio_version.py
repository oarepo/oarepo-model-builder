from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioVersionBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_version"
    section = "version"
    template = "invenio_version"

    def _get_output_module(self):
        return f"{self.current_model.definition['module']['qualified']}.version"
