import marshmallow as ma
from marshmallow import fields

from .model_validation import model_validator
from .utils import ExtendablePartSchema


class ImportSchema(ExtendablePartSchema):
    _import = fields.String(data_key="import", required=True)
    alias = fields.String(required=False)


class PropertyMarshmallowSchema(ExtendablePartSchema):
    read = fields.Boolean(required=False)
    write = fields.Boolean(required=False)
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    field_name = fields.String(data_key="field-name", required=False)
    field = fields.String(required=False)
    field_class = fields.String(data_key="field-class", required=False)
    arguments = fields.List(fields.String(), required=False)
    validators = fields.List(fields.String(), required=False)


class ModelMarshmallowSchema(ma.Schema):
    class ObjectOnlyMarshmallowProps(ExtendablePartSchema):
        imports = fields.List(
            fields.Nested(ImportSchema), required=False
        )  # imports must be here as well as it is used on model's root (without field)
        generate = fields.Boolean(required=False)
        schema_class = fields.String(data_key="schema-class", required=False)
        base_classes = fields.List(
            fields.String(), data_key="base-classes", required=False
        )

    marshmallow = fields.Nested(
        lambda: model_validator.validator_class("property-marshmallow-model")()
    )


class ObjectPropertyMarshmallowSchema(ma.Schema):
    class ObjectMarshmallowProps(
        ModelMarshmallowSchema.ObjectOnlyMarshmallowProps,
        PropertyMarshmallowSchema,
    ):
        pass

    marshmallow = fields.Nested(
        lambda: model_validator.validator_class("property-marshmallow-object")()
    )
