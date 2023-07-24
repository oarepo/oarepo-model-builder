from typing import List

from ..datatypes.components.facets import FacetDefinition
from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search_options"
    section = "search-options"
    template = "record-search-options"

    def finish(self, **extra_kwargs):
        facets: List[FacetDefinition] = []
        for node in self.current_model.deep_iter():
            facets.extend(node.section_facets.config["facets"])
        search_data = []
        for f in facets:
            search_data.append({f.path: "facets." + f.path})
        if "sortable" in self.current_model.definition:
            sort_options = self.current_model.definition["sortable"]
        extra_kwargs["search_data"] = search_data
        extra_kwargs["sort_definition"] = sort_options
        super().finish(**extra_kwargs)
