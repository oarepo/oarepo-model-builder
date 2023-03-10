from marshmallow import fields

from .model_validation import model_validator
from .utils import ExtendablePartSchema


class RootSchema(ExtendablePartSchema):
    model = fields.Nested(lambda: model_validator.validator_class("model")())
    settings = fields.Nested(lambda: model_validator.validator_class("settings")())
    version = fields.String(required=False, dump_default="1.0.0")
    title = fields.String(required=False)
    output_directory = fields.String(data_key="output-directory", required=False)
    defs = fields.Nested(
        lambda: model_validator.validator_class("properties")(), data_key="$defs"
    )
    runtime_dependencies = fields.Dict(
        fields.String(),
        fields.String(),
        required=False,
        data_key="runtime-dependencies",
    )
    dev_dependencies = fields.Dict(
        fields.String(), fields.String(), required=False, data_key="dev-dependencies"
    )
