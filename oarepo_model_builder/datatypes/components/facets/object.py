from oarepo_model_builder.datatypes import ObjectDataType, NestedDataType, datatypes
from .field import RegularFacetsComponent


class ObjectFacetsComponent(RegularFacetsComponent):


    eligible_datatypes = [ObjectDataType]
    def build_definition(self,datatype,  facets, facetka = None):
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facetka=facetka
        )
    def build_facets(self, datatype, facets, facetka):
        print("objeect")
        # for c in datatype.children.values():
        #     datatypes.call_components(
        #         c,
        #         "build_facets",
        #         facets=facets,
        #     )
        # facet_section = datatype.section_facets
        # facets.append(facet_section.config)
        # print(facet_section.config)