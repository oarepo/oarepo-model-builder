import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import ImportSchema

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

    class Meta:
        unknown = ma.RAISE


class PermissionsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        permissions = ma.fields.Nested(
            ModelPermissionsSchema(),
            required=False,
            metadata={"doc": "Permissions settings"},
        )

    def before_model_prepare(self, datatype, **kwargs):
        module = datatype.definition["module"]
        profile_module = datatype.definition["profile-module"]
        record_prefix = datatype.definition["record-prefix"]
        record_services_module = datatype.definition["record-services-module"]

        permissions = set_default(dataset, "permissions", {})
        permissions.setdefault("generate", False)
        permissions.setdefault("presets", [])
        permissions.setdefault("extra-code", "")
        if permissions["generate"]:
            permissions.setdefault(
                "class",
                f"{record_services_module}.permissions.{record_prefix}PermissionPolicy",
            )
            permissions.setdefault(
                "base-classes",
                [],
            )
