import marshmallow as ma
from marshmallow import fields
from .model_validation import model_validator
from marshmallow_union import Union

from .utils import CheckedConstant


class PluginsSchema(ma.Schema):
    packages = fields.List(fields.String())
    output = fields.Nested(
        lambda: model_validator.validator_class("plugin-schema")(), required=False
    )
    builder = fields.Nested(
        lambda: model_validator.validator_class("plugin-schema")(), required=False
    )
    model = fields.Nested(
        lambda: model_validator.validator_class("plugin-schema")(), required=False
    )
    property = fields.Nested(
        lambda: model_validator.validator_class("plugin-schema")(), required=False
    )


class PluginConfigSchema(ma.Schema):
    disable = Union(CheckedConstant("__all__"), fields.List(fields.String()))
    enable = fields.List(fields.String())
    include = fields.List(fields.String())
