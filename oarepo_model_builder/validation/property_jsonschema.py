from marshmallow import fields

from .utils import PermissiveSchema


class PropertyJSONSchema(PermissiveSchema):
    generate = fields.Boolean(dump_default=True)
