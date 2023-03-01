from marshmallow import fields

from .model_validation import model_validator
from .utils import ExtendablePartSchema


class ModelUISchema(ExtendablePartSchema):
    i18n_prefix = fields.String(data_key="i18n-prefix")


class PropertyUISchema(ExtendablePartSchema):
    i18n_prefix = fields.String(data_key="i18n-prefix")
    marshmallow = fields.Nested(
        lambda: model_validator.validator_class("property-marshmallow-object")()
    )
