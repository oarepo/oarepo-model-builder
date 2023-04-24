from ..marshmallow import ObjectMarshmallowExtraSchema

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType


ModelMarshmallowSchema = ObjectMarshmallowExtraSchema


class MarshmallowModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        marshmallow = ma.fields.Nested(ModelMarshmallowSchema)
