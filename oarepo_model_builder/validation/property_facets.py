from marshmallow import fields

from .utils import ExtendablePartSchema


class PropertyFacets(ExtendablePartSchema):
    clazz = fields.String(data_key="class", required=False)
    field = fields.String(required=False)
