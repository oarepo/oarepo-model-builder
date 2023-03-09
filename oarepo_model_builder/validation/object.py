import marshmallow as ma
from marshmallow import fields


class AdditionalPropertiesSchema(ma.Schema):
    type = fields.String(required=True)


class PropertyNamesSchema(ma.Schema):
    pattern = fields.String(required=True)


class ObjectDynamicSchema(ma.Schema):
    additionalProperties = fields.Nested(AdditionalPropertiesSchema, required=False)
    propertyNames = fields.Nested(PropertyNamesSchema, required=False)
