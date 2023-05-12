from oarepo_model_builder.datatypes import ObjectDataType, NestedDataType, datatypes, ArrayDataType
from .field import RegularFacetsComponent


class ArrayFacetsComponent(RegularFacetsComponent):


    eligible_datatypes = [ArrayDataType]

    def build_definition(self, datatype, facets, facetka=None):
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facetka=facetka
        )
    def build_facets(self, datatype, facets, facetka = None):
        print("aray fieeeld")
        facet_section = datatype.section_facets
        if not facet_section.config == {}:
            facetka = {'path' : datatype.path, 'class' :  datatype.section_facets.config['facet_class'] + f'(field=\"{datatype.path}\"' + ')'}
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facetka = facetka
        )
    # def build_facets(self, datatype, facets, facetka = None):
    #     print("araay")
    #     for c in datatype.item.children.values():
    #         datatypes.call_components(
    #             c,
    #             "build_facets",
    #             facets=facets,
    #         )
    #     # facet_section = datatype.section_facets
    #     # facets.append(facet_section.config)
    #     # print(facet_section.config)