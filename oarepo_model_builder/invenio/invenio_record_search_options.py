from collections import defaultdict
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
        facet_groups, default_group, sort_options = facet_data(
            facets, self.current_model
        )

        extra_kwargs["facet_groups"] = facet_groups
        extra_kwargs["default_group"] = default_group
        extra_kwargs["sort_definition"] = sort_options
        super().finish(**extra_kwargs)


def facet_data(facets, current_model):
    facet_groups = {}
    default_group = []
    search_data = []

    # gather all facet group names
    facet_group_names = set()
    for f in facets:
        facet_group_names.update(f.facet_groups.keys())

    top_level_facet_groups = current_model.definition.get("facets", {}).get(
        "facet-groups", {}
    )
    facet_group_names.update(top_level_facet_groups.keys())
    path_to_facet_group = defaultdict(dict)

    for group, group_def in top_level_facet_groups.items():
        for path, priority in group_def.items():
            path_to_facet_group[group][path] = priority

    # for each group name, gather all facets with that group name
    # sort them by their order in the group
    # and add them to the facet_groups dict
    for group in sorted(facet_group_names):
        # skip the default group
        if group == "_default":
            continue

        # gather all facets with this facet_group_name
        group_members = []
        for f in facets:
            if group in f.facet_groups:
                group_members.append((f, f.facet_groups[group]))

            # if there is a definition of facet groups on the model's facets -> add the selected facets as well
            for path, priority in path_to_facet_group.get(group, {}).items():
                if f.dot_path.startswith(path):
                    group_members.append((f, priority))

        # sort the group members by their order in the facet_group
        group_members.sort(key=lambda x: x[1])

        if group not in facet_groups.keys():
            facet_groups[group] = {}

        for f, _ in group_members:
            facet_groups[group][f.path] = "facets." + f.path

    for f in facets:
        if len(f.facet_groups) > 0:
            default_group.append({f.path: "facets." + f.path})
        search_data.append({f.path: "facets." + f.path})

    if "sortable" in current_model.definition:
        sort_options = current_model.definition["sortable"]
    else:
        sort_options = {}
    return facet_groups, default_group, sort_options
