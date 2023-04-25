import marshmallow as ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class CheckedConstant(fields.Constant):
    def _deserialize(self, value, *args, **kwargs):
        if value != self.constant:
            raise ValidationError(f"Bad value: '{self.constant}' expected.")
        return super()._deserialize(value, *args, **kwargs)


class ExtendablePartSchema(ma.Schema):
    extend = fields.String(required=False)
    use = fields.String(required=False)


class PermissiveSchema(ExtendablePartSchema):
    class Meta:
        unknown = ma.INCLUDE

    def dump(self, obj, *, many=None):
        if not obj:
            return super().dump(obj, many=many)
        if many:
            return [self.dump(x, many=False) for x in obj]
        return {**obj, **super().dump(obj, many=False)}


class StrictSchema(ExtendablePartSchema):
    class Meta:
        unknown = ma.RAISE


class ImportSchema(ExtendablePartSchema):
    _import = fields.String(data_key="import", attribute="import", required=True)
    alias = fields.String(required=False)
