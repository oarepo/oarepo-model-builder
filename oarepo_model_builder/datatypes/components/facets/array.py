from oarepo_model_builder.datatypes import ArrayDataType, datatypes
from oarepo_model_builder.utils.facet_helpers import facet_name

from .field import RegularFacetsComponent


class ArrayFacetsComponent(RegularFacetsComponent):
    eligible_datatypes = [ArrayDataType]

    def build_definition(
        self, datatype, facets, facet_definition=None, searchable=True
    ):
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
        if hasattr(datatype.item, "facets"):
            facet_section = datatype.item.facets
            _path = datatype.path
            if "keyword" in facet_section:
                _path = _path + ".keyword"
            if "path" in facet_section:
                path = _path + "." + facet_section["path"]
            else:
                path = _path
            key = facet_section.get("key", facet_name(_path))
            label = facet_section.get("label", f'{_path.replace(".", "/")}.label')
            imports = facet_section.get("imports", [])
            arguments = facet_section.get("args", [])
            arguments_string = ",".join(arguments)
            if arguments_string != "":
                arguments_string = "," + arguments_string
            facet_searchable = facet_section.get("searchable", searchable)
            field = facet_section.get(
                "field",
                facet_section["facet_class"]
                + f'(field="{path}", label =_("{label}") {arguments_string} '
                + ")",
            )
            facet_definition = {
                "path": key,
                "class": field,
                "facet_searchable": facet_searchable,
                "imports": imports,
            }

        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facet_definition=facet_definition,
            searchable=searchable,
        )
