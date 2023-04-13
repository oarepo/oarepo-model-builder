from marshmallow import fields

from oarepo_model_builder.validation.property_marshmallow import ImportSchema

from .utils import ExtendablePartSchema


class PropertyFacets(ExtendablePartSchema):
    key = fields.String(required=False)
    field = fields.String(required=False)
    searchable = fields.Boolean(required=False)
    facet_class = fields.String(required=False, data_key="facet-class")
    args = fields.List(fields.String(), required=False)
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    path = fields.String(required=False)
