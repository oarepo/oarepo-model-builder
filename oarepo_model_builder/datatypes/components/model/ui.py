import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType

from ..ui import ObjectUIComponent, ObjectUIExtraSchema
from .marshmallow import ModelMarshmallowSchema


class ModelUISchema(ObjectUIExtraSchema):
    marshmallow = ma.fields.Nested(ModelMarshmallowSchema)
    serializer_class = ma.fields.String(
        attribute="serializer-class",
        data_key="serializer-class",
        metadata={"doc": "UI serializer class qualified name"},
    )


class UIModelComponent(ObjectUIComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(ModelUISchema, metadata={"doc": "UI settings"})
