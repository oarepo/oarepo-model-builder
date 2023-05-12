from oarepo_model_builder.datatypes import ObjectDataType, NestedDataType, datatypes
from .field import RegularFacetsComponent
from .object import ObjectFacetsComponent


class NestedFacetsComponent(ObjectFacetsComponent):


    eligible_datatypes = [NestedDataType]

    def build_definition(self, datatype, facets, facetka=None):
        inner_facetka = facetka['class']
        facetka['class'] = f'NestedLabeledFacet(path = {datatype.path}, nested = {inner_facetka})'
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facetka=facetka
        )
    def build_facets(self, datatype, facets, facetka):
        print(facetka)
        # print("nesteeed")
        # facet_section = datatype.section_facets
        # stack = []
        # nest = False
        # if not inner:
        #     inner = []
        # else:
        #     nest = True
        #     for i in inner:
        #         stack.append(i)
        #     inner = []
        #
        #
        # for c in datatype.children.values():
        #     datatypes.call_components(
        #         c,
        #         "build_facets",
        #         facets=facets,
        #         # inner = inner
        #     )
        # nested_facets = self.create_nest(facet_section.config, datatype, inner)
        # if not nest:
        #     for i in nested_facets:
        #         facets.append(i)
        # else:
        #     for i in nested_facets:
        #         inner.append(i)
        #     for x in stack:
        #         inner.append(x)
        #     # inner = stack
        #     # return inner
        # print("nested after")
        #
        # facet_section = datatype.section_facets
        # facets.append(facet_section.config)
        # print(facet_section.config)
    def create_nest(self, config,datatype, inner):
        nested_facets = []
        for i in inner:
            for x in i:
                nested_facets.append({x: config['facet_class'] + f'(path=\"{datatype.path}\" nested = {i[x]}' + ')'})
        return nested_facets