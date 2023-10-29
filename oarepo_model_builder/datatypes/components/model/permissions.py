import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import parent_module
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .service import ServiceModelComponent
from .utils import set_default


class ModelPermissionsSchema(ma.Schema):
    generate = ma.fields.Bool(
        metadata={"doc": "Set to true to generate the permissions class"}
    )
    presets = ma.fields.List(
        ma.fields.String(),
        metadata={
            "doc": "A list of presets that will be merged with the permissions class."
        },
    )
    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the generated class"},
    )
    base_classes = ma.fields.List(
        ma.fields.String(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "Base classes for the generated permission class"},
    )
    extra_code = ma.fields.String(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be copied below the permission class"},
    )
    module = ma.fields.String(
        metadata={"doc": "Module where the permissions will be placed"}
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    skip = ma.fields.Boolean()

    class Meta:
        unknown = ma.RAISE


class PermissionsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, ServiceModelComponent]

    class ModelSchema(ma.Schema):
        permissions = ma.fields.Nested(
            ModelPermissionsSchema(),
            required=False,
            metadata={"doc": "Permissions settings"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        prefix = datatype.definition["module"]["prefix"]
        record_services_module = parent_module(datatype.definition["service"]["module"])

        permissions = set_default(datatype, "permissions", {})
        permissions.setdefault("generate", True)
        permissions.setdefault("presets", ["everyone"])
        permissions.setdefault("extra-code", "")
        permissions_module = permissions.setdefault(
            "module",
            f"{record_services_module}.permissions",
        )
        permissions.setdefault(
            "class",
            f"{permissions_module}.{prefix}PermissionPolicy",
        )
        permissions.setdefault(
            "base-classes",
            ["invenio_records_permissions.RecordPermissionPolicy"],
        )
        permissions.setdefault(
            "imports",
            [],
        )
