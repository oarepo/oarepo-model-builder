from oarepo_model_builder.datatypes import NestedDataType, datatypes

from .object import ObjectFacetsComponent


class NestedFacetsComponent(ObjectFacetsComponent):
    eligible_datatypes = [NestedDataType]

    def build_definition(
        self, datatype, facets, facet_definition=None, searchable=True
    ):
        inner_facet_definition = facet_definition["class"]
        facet_section = datatype.section_facets.config
        if facet_section != {}:
            _path = datatype.path
            if "path" in facet_section:
                path = _path + "." + facet_section["path"]
            else:
                path = _path

            facet_searchable = facet_section.get("searchable", "")
            if facet_definition:
                fs = facet_definition.get("facet_searchable", "")
                if fs != "" and facet_searchable != "" and fs != facet_searchable:
                    facet_definition["facet_searchable"] = facet_searchable
                imports = facet_section.get("imports", [])
                arguments = facet_section.get("args", [])
                arguments_string = ",".join(arguments)
                if arguments_string != "":
                    arguments_string = "," + arguments_string
                facet_definition["imports"].extend(imports)
                facet_definition["class"] = facet_section.get(
                    "field",
                    f'{datatype.section_facets.config["facet_class"]}(path = "{path}", nested_facet = {inner_facet_definition} {arguments_string})',
                )
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facet_definition=facet_definition,
            searchable=searchable,
        )

    def build_facets(self, datatype, facets, facet_definition=None, searchable=True):
        pass
