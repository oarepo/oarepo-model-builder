import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import DataTypeComponent, ObjectDataType
from oarepo_model_builder.validation.utils import StrictSchema

from .marshmallow import ObjectMarshmallowSchema, PropertyMarshmallowSchema


class PropertyUISchema(StrictSchema):
    marshmallow = fields.Nested(PropertyMarshmallowSchema)


class RegularUIComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(
            PropertyUISchema,
            required=False,
        )


class ObjectUIExtraSchema(ma.Schema):
    marshmallow = fields.Nested(ObjectMarshmallowSchema)


class ObjectUISchema(ObjectUIExtraSchema, PropertyUISchema):
    pass


class ObjectUIComponent(RegularUIComponent):
    eligible_datatypes = [ObjectDataType]

    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(ObjectUISchema)
