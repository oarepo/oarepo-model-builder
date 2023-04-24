import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent


class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    searchable = ma.fields.Bool(required=False)


class RegularFacetsComponent(DataTypeComponent):
    eligible_datatypes = []

    class ModelSchema(ma.Schema):
        facets = ma.fields.Nested(
            FacetsSchema,
            required=False,
        )
