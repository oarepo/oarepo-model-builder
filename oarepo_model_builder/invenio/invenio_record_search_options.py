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
        facet_groups = {}
        default_group = []
        search_data = []
        for f in facets:
            for group in f.facet_groups:
                if group != 'default':
                    if group not in facet_groups.keys():
                        facet_groups[group] = {}
                    facet_groups[group][f.path] = "facets." + f.path
                if group == 'default':
                    default_group.append({f.path: "facets." + f.path})
            search_data.append({f.path: "facets." + f.path})
        if "sortable" in self.current_model.definition:
            sort_options = self.current_model.definition["sortable"]
        else:
            sort_options = {}
        extra_kwargs["facet_groups"] = facet_groups
        extra_kwargs["default_group"] = default_group
        extra_kwargs["sort_definition"] = sort_options
        super().finish(**extra_kwargs)
