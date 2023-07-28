from typing import List

from ..datatypes.components.facets import FacetDefinition
from .invenio_base import InvenioBaseClassPythonBuilder
from .invenio_record_facets import get_distinct_facets


class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search_options"
    section = "search-options"
    template = "record-search-options"

    def finish(self, **extra_kwargs):
        facets: List[FacetDefinition] = get_distinct_facets(self.current_model)

        search_data = []
        for f in facets:
            search_data.append({f.path: "facets." + f.path})
        if "sortable" in self.current_model.definition:
            sort_options = self.current_model.definition["sortable"]
        else:
            sort_options = {}
        extra_kwargs["search_data"] = search_data
        extra_kwargs["sort_definition"] = sort_options
        super().finish(**extra_kwargs)
