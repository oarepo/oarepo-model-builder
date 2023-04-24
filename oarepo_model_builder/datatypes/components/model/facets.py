import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType

from ..facets import RegularFacetsComponent


class FacetsModelComponent(RegularFacetsComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        class Meta:
            unknown = ma.RAISE

        searchable = ma.fields.Bool()
