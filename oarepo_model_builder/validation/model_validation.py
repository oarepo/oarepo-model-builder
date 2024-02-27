import marshmallow as ma

from .extensibility import ExtensibleSchema
from .plugins import PluginsSchema


def get_model_schema():
    from ..datatypes.model import ModelDataType

    return ModelDataType.validator()


class DefsSchema(ma.Schema):
    class Meta:
        unknown = ma.INCLUDE


class SettingsPythonSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    use_isort = ma.fields.Bool(
        attribute="use-isort", data_key="use-isort", load_default=True
    )
    use_black = ma.fields.Bool(
        attribute="use-black", data_key="use-black", load_default=True
    )
    use_autoflake = ma.fields.Bool(
        attribute="use-autoflake", data_key="use-autoflake", load_default=True
    )


class SettingsOpenSearchSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    version = ma.fields.String(load_default="os-v2")


class MarshmallowSettingsSchema(ma.Schema):
    schema_base_class = ma.fields.String(
        attribute="schema-base-class",
        data_key="schema-base-class",
        default="oarepo_runtime.services.schema.marshmallow.DictOnlySchema",
    )
    ui_schema_base_class = ma.fields.String(
        attribute="ui-schema-base-class",
        data_key="ui-schema-base-class",
        default="oarepo_runtime.services.schema.marshmallow.DictOnlySchema",
    )


class SettingsSchema(ma.Schema):
    python = ma.fields.Nested(ExtensibleSchema("settings.python", SettingsPythonSchema))
    opensearch = ma.fields.Nested(
        ExtensibleSchema("settings.opensearch", SettingsOpenSearchSchema)
    )
    schema_server = ma.fields.String(
        attribute="schema-server", data_key="schema-server", load_default="local://"
    )
    extension_elements = ma.fields.List(
        ma.fields.String(),
        attribute="extension-elements",
        data_key="extension-elements",
    )
    marshmallow = ma.fields.Nested(
        MarshmallowSettingsSchema,
        load_default=lambda: {
            "schema-base-class": "oarepo_runtime.services.schema.marshmallow.DictOnlySchema",
            "ui-schema-base-class": "oarepo_runtime.services.schema.marshmallow.DictOnlySchema",
        },
    )

    class Meta:
        unknown = ma.RAISE


class ModelFileSchema(ma.Schema):
    version = ma.fields.Str(
        load_default="1.0.0", metadata={"doc": "Model version, default value 1.0.0"}
    )
    record = ma.fields.Nested(get_model_schema, metadata={"doc": "Main record"})
    defs = ma.fields.Nested(
        DefsSchema,
        attribute="$defs",
        data_key="$defs",
        metadata={"doc": "Extra definitions, might be included via _use_ or _extend_"},
    )
    settings = ma.fields.Nested(
        ExtensibleSchema("settings", SettingsSchema),
        metadata={"doc": "General settings, applies to all generated sources"},
        load_default=lambda: SettingsSchema().load({}),
    )
    runtime_dependencies = ma.fields.Dict(
        ma.fields.String(),
        ma.fields.String(),
        attribute="runtime-dependencies",
        data_key="runtime-dependencies",
    )
    dev_dependencies = ma.fields.Dict(
        ma.fields.String(),
        ma.fields.String(),
        attribute="dev-dependencies",
        data_key="dev-dependencies",
    )
    plugins = ma.fields.Nested(
        ExtensibleSchema("plugins", PluginsSchema),
        metadata={"doc": "Plugins to load, enable, disable"},
    )
    profiles = ma.fields.List(ma.fields.String())


class ModelValidator:
    def validate(self, data):
        complete_model_schema = ExtensibleSchema("model_file", ModelFileSchema)
        validator = complete_model_schema()
        return validator.load(data)


model_validator = ModelValidator()
