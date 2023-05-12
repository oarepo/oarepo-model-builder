import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType


class PluginEnableDisableField(ma.fields.List):
    def deserialize(self, value, attr, data, **kwargs):
        if value == "__all__":
            return value
        return super().deserialize(value, attr, data, **kwargs)


class PluginSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    packages = ma.fields.List(ma.fields.String())
    include = ma.fields.List(ma.fields.String())
    enable = PluginEnableDisableField(ma.fields.String())
    disable = PluginEnableDisableField(ma.fields.String())


class PluginsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    output = ma.fields.Nested(PluginSchema)


class PluginsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        plugins = ma.fields.Nested(PluginsSchema)
