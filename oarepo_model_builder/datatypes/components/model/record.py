import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import convert_config_to_qualified_name
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .utils import set_default


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
    skip = ma.fields.Boolean()
    fields = ma.fields.Dict(
        attribute="fields",
        data_key="fields",
        metadata={"doc": "Extra fields to add to the class"},
    )


class RecordModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        record = ma.fields.Nested(
            RecordClassSchema, metadata={"doc": "api/Record settings"}
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        module = datatype.definition["module"]["qualified"]
        profile_module = context["profile_module"]
        record_prefix = datatype.definition["module"]["prefix"]

        record = set_default(datatype, "record", {})
        record.setdefault("generate", True)
        records_module = record.setdefault("module", f"{module}.{profile_module}.api")
        record.setdefault("class", f"{records_module}.{record_prefix}Record")
        record.setdefault(
            "base-classes",
            ["invenio_records_resources.records.api.Record{InvenioRecord}"],
        )
        record.setdefault(
            "imports",
            [],
        )
        record.setdefault("extra-code", "")
        record.setdefault("fields", {})
        convert_config_to_qualified_name(record)
