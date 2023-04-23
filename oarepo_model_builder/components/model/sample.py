from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
import marshmallow as ma
from ..sample import RegularSampleComponent
from ...validation.utils import StrictSchema


class SampleSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    count = ma.fields.Int()


class SampleModelComponent(RegularSampleComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(StrictSchema):
        sample = ma.fields.Nested(
            SampleSchema,
            required=False,
        )
