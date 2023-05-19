import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.validation.utils import StrictSchema

from ..sample import RegularSampleComponent
from .utils import set_default


class SampleSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    count = ma.fields.Int(metadata={"doc": "Number of generated records"})
    file_ = ma.fields.Str(
        attribute="file",
        data_key="file",
        metadata={"doc": "File into which the records will be generated"},
    )


class SampleModelComponent(RegularSampleComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(StrictSchema):
        sample = ma.fields.Nested(
            SampleSchema, metadata={"doc": "Settings for sample document generator"}
        )

    def before_model_prepare(self, datatype, **kwargs):
        sample = set_default(datatype, "sample", {})
        sample.setdefault("file", "data/sample_data.yaml")
