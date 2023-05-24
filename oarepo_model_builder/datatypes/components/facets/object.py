from oarepo_model_builder.datatypes import ObjectDataType, datatypes

from .field import RegularFacetsComponent


class ObjectFacetsComponent(RegularFacetsComponent):
    eligible_datatypes = [ObjectDataType]

    def build_definition(
        self, datatype, facets, facet_definition=None, searchable=True
    ):
        if datatype.key is not None:
            facet_section = datatype.section_facets.config
            if facet_section != {}:
                facet_searchable = facet_section.get("searchable", "")
                if facet_definition:
                    imports = facet_section.get("imports", [])
                    facet_definition["imports"].extend(imports)
                    fs = facet_definition.get("facet_searchable", "")
                    if fs != "" and facet_searchable != "" and fs != facet_searchable:
                        facet_definition["facet_searchable"] = facet_searchable
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facet_definition=facet_definition,
            searchable=searchable,
        )

    def build_facets(self, datatype, facets, facet_definition=None, searchable=True):
        pass
