from .invenio_base import InvenioBaseClassPythonBuilder

class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    output_builder_type = 'invenio_record_search'
    class_config = 'record-search-options-class'
    template = 'record-search-options'
