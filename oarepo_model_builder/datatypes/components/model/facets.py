import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.validation.utils import ImportSchema
from oarepo_model_builder.datatypes import DataType, datatypes
from oarepo_model_builder.datatypes import ModelDataType
class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    searchable = ma.fields.Bool(required=False)


class FacetsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        facets = ma.fields.Nested(
            FacetsSchema,
            required=False,
        )

    def after_model_prepare(self, *, datatype, context, **kwargs):
        print('kckkkkkkkkkkkkkkkkkk')
        facets = datatypes.call_components(
            datatype,
            "build_facets",
            facets=[],
            facetka = None
        )
        print(facets)
        print('fn?')



    def process_facets(self, datatype, section, **kwargs):
        print('gngngn')


    def build_facets(self, datatype, facets, facetka = None):

        for c in datatype.children.values():
            if c.model_type == 'array':
                children = c.item.children
            else:
                children = c.children
            if children != {}:
                self.get_leaf(children, facets)
            else:
                datatypes.call_components(
                    c,
                    "build_facets",
                    facets=facets,
                )

        # print(facets)
        return facets
    def get_leaf(self, children, facets):
        for c in children.values():
            if c.model_type == 'array':
                children = c.item.children
            else:
                children = c.children
            if children != {}:
                self.get_leaf(children, facets)
            else:
                datatypes.call_components(
                    c,
                    "build_facets",
                    facets=facets,
                )
    def build_definition(self,datatype,  facets, facetka = None):
        # print(facetka)
        if facetka:
            facets.append(facetka)

# class RegularFacetsComponent(DataTypeComponent): #todo divnoimport?
#     eligible_datatypes = []
#
#     class ModelSchema(ma.Schema):
#         facets = ma.fields.Nested(
#             FacetsSchema,
#             required=False,
#         )
