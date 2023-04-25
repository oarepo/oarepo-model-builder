import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType

from ..ui import ObjectUIExtraSchema, ObjectUIComponent

ModelUISchema = ObjectUIExtraSchema


class UIModelComponent(ObjectUIComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(ModelUISchema)
