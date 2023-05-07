import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import ImportSchema


class RecordClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(
        metadata={"doc": "Set true to generate the class (default)"}
    )
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the class"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "Model base classes"},
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to copy to record file"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class RecordModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        record = ma.fields.Nested(
            RecordClassSchema, metadata={"doc": "api/Record settings"}
        )

    def before_model_prepare(self, datatype, **kwargs):
        module = datatype.definition["module"]
        profile_module = datatype.definition["profile-module"]
        record_prefix = datatype.definition["record-prefix"]

        record = setdefault(datatype, "record", {})
        record.setdefault("generate", True)
        records_module = record.setdefault("module", f"{module}.{profile_module}")
        record.setdefault("class", f"{records_module}.api.{record_prefix}Record")
        record.setdefault(
            "base-classes", ["invenio_records_resources.records.api.Record"]
        )
        record.setdefault("extra-code", "")
