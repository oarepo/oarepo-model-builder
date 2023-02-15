from marshmallow import fields

from .model_validation import model_validator
from .utils import ExtendablePartSchema


class SettingsSchema(ExtendablePartSchema):
    opensearch = fields.Nested(
        lambda: model_validator.validator_class("settings-opensearch")()
    )

    python = fields.Nested(lambda: model_validator.validator_class("settings-python")())


class SettingsOpenSearchSchema(ExtendablePartSchema):
    version = fields.String(dump_default="os-v2")


class SettingsPythonSchema(ExtendablePartSchema):
    use_black = fields.Boolean(data_key="use-black", dump_default=True)
    use_isort = fields.Boolean(data_key="use-isort", dump_default=True)
    always_defined_import_prefixes = fields.List(
        fields.String(), data_key="always-defined-import-prefixes", required=False
    )
    templates = fields.Dict(fields.String(), fields.String())
