from marshmallow import fields
from .model_validation import model_validator
from marshmallow_union import Union

from .utils import ExtendablePartSchema


class Property(ExtendablePartSchema):
    facets = fields.Nested(lambda: model_validator.validator_class("property-facets")())
    sample = Union(
        [
            fields.String(),  # use this constant value for the sample data
            fields.List(fields.Boolean()),  # or array of booleans
            fields.List(fields.Integer()),  # or array of booleans
            fields.List(fields.Float()),  # or array of booleans
            fields.List(fields.String()),  # or array of strings
            fields.Nested(lambda: model_validator.validator_class("property-sample")()),
        ],
        required=False,
    )
    jsonschema = fields.Nested(
        lambda: model_validator.validator_class("property-jsonschema")()
    )
    mapping = fields.Nested(
        lambda: model_validator.validator_class("property-mapping")()
    )
    marshmallow = fields.Nested(
        lambda: model_validator.validator_class("property-marshmallow")()
    )
    sortable = fields.Nested(
        lambda: model_validator.validator_class("property-sortable")()
    )


class ObjectProperty(ExtendablePartSchema):
    required = fields.Boolean(required=False)
