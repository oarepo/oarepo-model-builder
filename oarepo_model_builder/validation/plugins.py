import marshmallow as ma


class PluginEnableDisableField(ma.fields.List):
    def deserialize(self, value, attr, data, **kwargs):
        if value == "__all__":
            return value
        return super().deserialize(value, attr, data, **kwargs)


class PluginSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    include = ma.fields.List(ma.fields.String())
    enable = PluginEnableDisableField(ma.fields.String())
    disable = PluginEnableDisableField(ma.fields.String())


class PluginsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    packages = ma.fields.List(ma.fields.String())
    output = ma.fields.Nested(PluginSchema)
    builder = ma.fields.Nested(PluginSchema)
