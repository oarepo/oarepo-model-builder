import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import parent_module
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .record import RecordModelComponent
from .utils import set_default


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
    skip = ma.fields.Boolean()


class RecordDumperModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, RecordModelComponent]

    class ModelSchema(ma.Schema):
        record_dumper = ma.fields.Nested(
            RecordDumperClassSchema,
            attribute="record-dumper",
            data_key="record-dumper",
            metadata={"doc": "Settings for record dumper"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        record_module = parent_module(datatype.definition["record"]["module"])
        prefix = datatype.definition["module"]["prefix"]

        dumper = set_default(datatype, "record-dumper", {})
        dumper.setdefault("generate", True)

        dumper_module = dumper.setdefault("module", f"{record_module}.dumpers.dumper")
        dumper.setdefault("class", f"{dumper_module}.{prefix}Dumper")
        dumper.setdefault(
            "base-classes", ["oarepo_runtime.records.dumpers.SearchDumper"]
        )
        dumper.setdefault("extra-code", "")
        dumper.setdefault("extensions", [])
        dumper.setdefault("imports", [])
