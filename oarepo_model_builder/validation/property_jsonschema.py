import marshmallow as ma
from marshmallow import fields

from .utils import ExtendablePartSchema


class PropertyJSONSchema(ExtendablePartSchema):
    generate = fields.Boolean(dump_default=True)

    class Meta:
        unknown = ma.INCLUDE
