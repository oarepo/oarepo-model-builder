from ..ui import ObjectUIExtraSchema

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType


ModelUISchema = ObjectUIExtraSchema


class UIModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(ModelUISchema)
