import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import (
    convert_config_to_qualified_name,
    package_name,
)
from oarepo_model_builder.validation.utils import ImportSchema

from .app import AppModelComponent
from .defaults import DefaultsModelComponent
from .service import ServiceModelComponent
from .utils import set_default


class RecordListClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Generate the record list class"})
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the record list class"},
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
        metadata={"doc": "Extra code to be put below the record list class"},
    )
    components = ma.fields.List(
        ma.fields.String(), metadata={"doc": "List of record list components"}
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    skip = ma.fields.Boolean()


class RecordListModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, AppModelComponent, ServiceModelComponent]

    class ModelSchema(ma.Schema):
        record_list = ma.fields.Nested(
            RecordListClassSchema,
            attribute="record-list",
            data_key="record-list",
            metadata={"doc": "Record list class settings"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        record_prefix = datatype.definition["module"]["prefix"]

        service_package = package_name(datatype.definition["service-config"]["module"])

        record_list_config = set_default(datatype, "record-list", {})

        record_list_config.setdefault("generate", True)
        record_list_module = record_list_config.setdefault(
            "module",
            f"{service_package}.results",
        )
        record_list_config.setdefault(
            "class",
            f"{record_list_module}.{record_prefix}RecordList",
        )
        record_list_config.setdefault("extra-code", "")
        record_list_config.setdefault(
            "base-classes",
            [
                "oarepo_runtime.services.results.RecordList",
            ],
        )
        record_list_config.setdefault("components", [])
        record_list_config.setdefault(
            "imports",
            [],
        )
        convert_config_to_qualified_name(record_list_config)
