from marshmallow import fields

from .utils import ExtendablePartSchema


class PropertyFacets(ExtendablePartSchema):
    key = fields.String(required=False)
    field = fields.String(required=False)
    searchable = fields.Boolean(required=False)
