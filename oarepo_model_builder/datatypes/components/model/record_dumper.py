import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import ImportSchema


class RecordDumperClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Generate the dumper class"})
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the class"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "List of base classes"},
    )
    extensions = ma.fields.List(
        ma.fields.Str(), metadata={"doc": "List of dumper extensions"}
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be copied to the bottom of the dumper file"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class RecordDumperModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        record_dumper = ma.fields.Nested(
            RecordDumperClassSchema,
            attribute="record-dumper",
            data_key="record-dumper",
            metadata={"doc": "Settings for record dumper"},
        )

    def before_model_prepare(self, datatype, **kwargs):
        module = datatype.definition["module"]
        profile_module = datatype.definition["profile-module"]
        record_prefix = datatype.definition["record-prefix"]

        dumper = setdefault(datatype, "record-metadata", {})
        dumper.setdefault("generate", True)

        records_module = metadata.setdefault("module", f"{module}.{profile_module}")
        dumper.setdefault("class", f"{records_module}.dumper.{record_prefix}Dumper")
        dumper.setdefault("base-classes", [])
        dumper.setdefault("extra-code", "")
        dumper.setdefault("extensions", [])
