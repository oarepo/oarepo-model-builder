import marshmallow as ma
from marshmallow import fields

from .model_validation import model_validator


class UIPropertyValidator(ma.Schema):
    marshmallow = fields.Nested(
        lambda: model_validator.validator_class("property-marshmallow")()
    )

    class Meta:
        unknown = ma.INCLUDE


class ObjectUIPropertyValidator(ma.Schema):
    marshmallow = fields.Nested(
        lambda: model_validator.validator_class("property-marshmallow-object")()
    )

    class Meta:
        unknown = ma.INCLUDE


class ObjectPropertyUISchema(ma.Schema):
    # x/[type object]
    ui = fields.Nested(lambda: model_validator.validator_class("object-property-ui")())
