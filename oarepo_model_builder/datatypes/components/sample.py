import marshmallow as ma

from oarepo_model_builder.datatypes import ArrayDataType, DataTypeComponent
from oarepo_model_builder.validation.utils import StrictSchema


class SampleSchema(StrictSchema):
    skip = ma.fields.Boolean(
        metadata={"doc": "Set true to skip generating sample for the field"}
    )
    faker = ma.fields.String(
        metadata={"doc": "The faker to use for generating the sample"}
    )
    params = ma.fields.Raw(metadata={"doc": "Params for the faker"})

    def load(
        self,
        data,
        *,
        many=None,
        partial=None,
        unknown=None,
    ):
        if isinstance(data, (list, tuple)):
            return data
        return super().load(data, many=many, partial=partial, unknown=unknown)

    def dump(self, obj, *, many=None):
        if many:
            return [self.dump(x, many=False) for x in obj]
        if isinstance(obj, (list, tuple)):
            return obj
        return super().dump(obj, many=False)


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
