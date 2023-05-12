import ma as ma

from oarepo_model_builder.utils.python_name import convert_name_to_python
from oarepo_model_builder.validation.utils import ImportSchema
from ... import KeywordDataType
import marshmallow as ma
from marshmallow import fields
from ...datatypes import DataType, Import, DataTypeComponent
from oarepo_model_builder.datatypes import datatypes
class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    searchable = ma.fields.Bool(required=False)
    key = fields.String(required=False)
    field = fields.String(required=False)
    facet_class = fields.String(required=False, data_key="facet-class")
    args = fields.List(fields.String(), required=False)
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    path = fields.String(required=False)




class RegularFacetsComponent( DataTypeComponent):
    eligible_datatypes = []

    class ModelSchema(ma.Schema):
        facets = ma.fields.Nested(
            FacetsSchema,
            required=False,
        )
    def build_facets(self, datatype, facets, facetka = None):
        print("fieeeld")
        facet_section = datatype.section_facets
        if not facet_section.config == {}:
            facetka = {'path' : datatype.path, 'class' :  datatype.section_facets.config['facet_class'] + f'(field=\"{datatype.path}\"' + ')'}
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facetka = facetka
        )
        # facet_def = ""
        # if not facet_section.config == {}:
        #     facet_def = self.create_definition(facet_section.config, datatype)
        #     if inner != None:
        #         inner.append(facet_def)
        #     else:
        #         facets.append(facet_def)
        # print(facet_section.config)


    def create_definition(self, config, datatype):

        return {datatype.path : config['facet_class'] + f'(field=\"{datatype.path}\"' + ')'}