import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.validation.utils import StrictSchema

from ..sample import RegularSampleComponent


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
