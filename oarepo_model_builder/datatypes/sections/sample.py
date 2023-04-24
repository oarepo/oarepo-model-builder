from oarepo_model_builder.datatypes import DataTypeComponent, ArrayDataType
import marshmallow as ma
from oarepo_model_builder.validation.utils import StrictSchema


class SampleSchema(StrictSchema):
    skip = ma.fields.Boolean()
    faker = ma.fields.String()
    params = ma.fields.Raw()


class RegularSampleComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        sample = ma.fields.Nested(
            SampleSchema,
            required=False,
        )


class ArraySampleSchema(StrictSchema):
    count = ma.fields.Int()


class ArraySampleComponent(RegularSampleComponent):
    eligible_datatypes = [ArrayDataType]

    class ModelSchema(StrictSchema):
        sample = ma.fields.Nested(
            ArraySampleSchema,
            required=False,
        )
