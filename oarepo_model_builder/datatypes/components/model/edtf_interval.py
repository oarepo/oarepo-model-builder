import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import parent_module
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .record_dumper import RecordDumperModelComponent
from .utils import set_default


class EDTFIntervalDumperClassSchema(ma.Schema):
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


class EDTFIntervalDumperModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [
        DefaultsModelComponent,
        RecordDumperModelComponent,
    ]

    class ModelSchema(ma.Schema):
        edtf_interval_dumper = ma.fields.Nested(
            EDTFIntervalDumperClassSchema,
            attribute="edtf-interval-dumper",
            data_key="edtf-interval-dumper",
            metadata={"doc": "Settings for edtf interval dumper"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        record_module = parent_module(datatype.definition["record"]["module"])
        prefix = datatype.definition["module"]["prefix"]

        dumper = set_default(datatype, "edtf-interval-dumper", {})
        dumper.setdefault("generate", True)

        dumper_module = dumper.setdefault("module", f"{record_module}.dumpers.edtf")
        ext_class = f"{dumper_module}.{prefix}EDTFIntervalDumperExt"
        dumper.setdefault("class", ext_class)
        dumper.setdefault(
            "base-classes",
            ["oarepo_runtime.records.dumpers.edtf_interval.EDTFIntervalDumperExt"],
        )
        dumper.setdefault("extra-code", "")
        dumper.setdefault("extensions", [])
        dumper.setdefault("imports", [])

        datatype.definition["record-dumper"]["extensions"].append(
            "{{" + ext_class + "}}()"
        )
