import marshmallow as ma
from marshmallow import fields

from .model_validation import model_validator
from .utils import CheckedConstant, ExtendablePartSchema, PermissiveSchema


class ModelSchema(ExtendablePartSchema):
    type = CheckedConstant("object", required=False)
    properties = fields.Nested(
        lambda: model_validator.validator_class("properties", strict=False)()
    )
    opensearch = fields.Nested(
        lambda: model_validator.validator_class("model-opensearch", strict=False)()
    )
    plugins = fields.Nested(
        lambda: model_validator.validator_class("plugins-schema")(), required=False
    )

    @ma.pre_load(pass_many=False)
    def set_properties_before_load(self, data, **kwargs):
        if not data.get("properties"):
            data = {**data}
            data["properties"] = {}
        return data


class ModelOpenSearchSchema(PermissiveSchema):
    pass
