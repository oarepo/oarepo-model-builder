import marshmallow as ma

from .extensibility import ExtensibleSchema


def get_model_schema():
    from ..datatypes.model import ModelDataType

    return ModelDataType.validator()


class DefsSchema(ma.Schema):
    class Meta:
        unknown = ma.INCLUDE


class SettingsPythonSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    use_isort = ma.fields.Bool(attribute="use-isort", data_key="use-isort")
    use_black = ma.fields.Bool(attribute="use-black", data_key="use-black")
    use_autoflake = ma.fields.Bool(attribute="use-autoflake", data_key="use-autoflake")


class SettingsOpenSearchSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    version = ma.fields.String(load_default="os-v2")


class SettingsSchema(ma.Schema):
    python = ma.fields.Nested(ExtensibleSchema("settings.python", SettingsPythonSchema))
    opensearch = ma.fields.Nested(
        ExtensibleSchema("settings.opensearch", SettingsOpenSearchSchema)
    )
    schema_version = ma.fields.String(
        attribute="schema-version", data_key="schema-version"
    )

    class Meta:
        unknown = ma.RAISE


class ModelFileSchema(ma.Schema):
    version = ma.fields.Str(load_default="1.0.0")
    model = ma.fields.Nested(get_model_schema)
    defs = ma.fields.Nested(DefsSchema, attribute="$defs", data_key="$defs")
    settings = ma.fields.Nested(ExtensibleSchema("settings", SettingsSchema))


class ModelValidator:

    def validate(self, data):
        validator = ModelFileSchema()
        return validator.load(data)


model_validator = ModelValidator()
