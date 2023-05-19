from .invenio_base import InvenioBaseClassPythonBuilder

OAREPO_FACETS_PROPERTY = "facets"
OAREPO_SORTABLE_PROPERTY = "sortable"


class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search"
    class_config = "record-search-options-class"
    template = None

    def begin(self, schema, settings):  # NOSONAR
        super().begin(schema, settings)
        self.template = "record-search-options"
        self.search_options_data = []
        self.sort_options_data = []
        self.facets_definition = []
        self.settings = settings
        self.facet_stack = []
        self.imports = set()

    def finish(self, **extra_kwargs):
        return
