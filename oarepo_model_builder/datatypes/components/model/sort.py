import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType

from .defaults import DefaultsModelComponent
from .record import RecordModelComponent


class SortSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    definition = ma.fields.String(required=False)


class SortModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, RecordModelComponent]

    class ModelSchema(ma.Schema):
        sortable = ma.fields.Nested(SortSchema, required=False)

    def before_model_prepare(self, datatype, *, context, **kwargs):
        prefix = datatype.definition["module"]["prefix"]
