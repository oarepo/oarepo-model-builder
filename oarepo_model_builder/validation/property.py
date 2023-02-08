import typing

from marshmallow import fields
from marshmallow.exceptions import ValidationError
from marshmallow_union import Union

from .model_validation import model_validator
from .utils import ExtendablePartSchema


class StrictString(fields.String):
    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if value is None or isinstance(value, str):
            return super()._deserialize(value, attr, data, **kwargs)
        raise ValidationError(
            f"String value expected, found {type(value)} with value {repr(value)[:30]}..."
        )

    def _serialize(self, value, attr, obj, **kwargs) -> typing.Union[str, None]:
        if value is None or isinstance(value, str):
            return super()._serialize(value, attr, obj, **kwargs)
        raise ValidationError(
            f"String value expected, found {type(value)} with value {repr(value)[:30]}..."
        )


class Property(ExtendablePartSchema):
    facets = fields.Nested(lambda: model_validator.validator_class("property-facets")())
    sample = Union(
        [
            fields.Nested(lambda: model_validator.validator_class("property-sample")()),
            fields.List(fields.Boolean()),  # or array of booleans
            fields.List(fields.Integer()),  # or array of booleans
            fields.List(fields.Float()),  # or array of booleans
            fields.List(fields.String()),  # or array of strings
            StrictString(),  # use this constant value for the sample data
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
