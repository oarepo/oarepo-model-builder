import marshmallow as ma
from marshmallow import fields

from .utils import ExtendablePartSchema, PermissiveSchema


class PropertyJSONSchema(PermissiveSchema):
    generate = fields.Boolean(dump_default=True)
