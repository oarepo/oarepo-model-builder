import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import (
    ArrayDataType,
    DataTypeComponent,
    ObjectDataType,
)
from oarepo_model_builder.validation.utils import (
    StrictSchema,
    ImportSchema,
    PermissiveSchema,
    StrictSchema,
)


class PropertyMarshmallowSchema(StrictSchema):
    read = fields.Boolean(required=False)
    write = fields.Boolean(required=False)
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    field_name = fields.String(
        data_key="field-name", attribute="field-name", required=False
    )
    field = fields.String(required=False)
    field_class = fields.String(
        data_key="field-class", attribute="field-class", required=False
    )
    arguments = fields.List(fields.String(), required=False)
    validators = fields.List(fields.String(), required=False)


class RegularMarshmallowComponent(DataTypeComponent):
    class MarshmallowSchema(ma.Schema):
        marshmallow = ma.fields.Nested(
            PropertyMarshmallowSchema,
            required=False,
        )


class ExtraField(ma.Schema):
    name = fields.String(required=True)
    value = fields.String(required=True)


class ObjectMarshmallowExtraSchema(ma.Schema):
    imports = fields.List(
        fields.Nested(ImportSchema), required=False
    )  # imports must be here as well as it is used on model's root (without field)
    generate = fields.Boolean(required=False)
    schema_class = fields.String(
        data_key="schema-class",
        attribute="schema-class",
        required=False,
        allow_none=True,
    )
    base_classes = fields.List(
        fields.String(),
        data_key="base-classes",
        attribute="base-classes",
        required=False,
    )
    extra_fields = fields.List(
        fields.Nested(ExtraField),
        required=False,
        data_key="extra-fields",
        attribute="extra-fields",
    )


class ObjectMarshmallowSchema(PropertyMarshmallowSchema, ObjectMarshmallowExtraSchema):
    pass


class ObjectMarshmallowComponent(DataTypeComponent):
    eligible_datatypes = [ObjectDataType]

    class MarshmallowSchema(ma.Schema):
        marshmallow = ma.fields.Nested(ObjectMarshmallowSchema)
