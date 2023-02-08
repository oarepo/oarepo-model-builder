import marshmallow as ma
from marshmallow import fields

from .utils import ExtendablePartSchema


class PropertySampleData(ExtendablePartSchema):
    skip = fields.Boolean(dump_default=False)
    faker = fields.String(required=False)
    params = fields.Raw(required=False)
    count = fields.Integer()


class ModelSampleConfiguration(ma.Schema):
    class RootSampleProps(ExtendablePartSchema):
        count = fields.Integer()

        class Meta:
            unknown = ma.RAISE

    sample = fields.Nested(RootSampleProps)
