import marshmallow as ma

from oarepo_model_builder.validation.utils import StrictSchema

from .containers import ObjectDataType
from .containers.object import ObjectMarshmallowExtraSchema

ModelMarshmallowSchema = ObjectMarshmallowExtraSchema


class ModelUISchema(StrictSchema):
    marshmallow = ma.fields.Nested(ModelMarshmallowSchema)


class ModelDataType(ObjectDataType):
    model_type = "model"
    schema_type = "object"

    class ModelSchema(ObjectDataType.ModelSchema):
        type = ma.fields.Str(
            load_default="model",
            required=False,
            validate=ma.validate.Equal("model"),
        )
        name = ma.fields.Str(attribute="model-name", data_key="model-name")
        package = ma.fields.Str(attribute="package", data_key="package")
        package_path = ma.fields.Str(attribute="package-path", data_key="package-path")
        profile_package = ma.fields.Str(
            attribute="profile-package", data_key="profile-package"
        )
        package_base_upper = ma.fields.Str(
            attribute="package-base-upper", data_key="package-base-upper"
        )
        kebap_package = ma.fields.Str(
            attribute="kebap-package", data_key="kebap-package"
        )
        package_base = ma.fields.Str(attribute="package-base", data_key="package-base")

        # base classes
        record_resource_bases = ma.fields.List(
            ma.fields.Str(),
            attribute="record-resource-bases",
            data_key="record-resource-bases",
        )
        record_resource_config_bases = ma.fields.List(
            ma.fields.Str(),
            attribute="record-resource-config-bases",
            data_key="record-resource-config-bases",
        )
        record_pid_provider_bases = ma.fields.List(
            ma.fields.Str(),
            attribute="record-pid-provider-bases",
            data_key="record-pid-provider-bases",
        )
        record_metadata_bases = ma.fields.List(
            ma.fields.Str(),
            attribute="record-metadata-bases",
            data_key="record-metadata-bases",
        )
        record_bases = ma.fields.List(
            ma.fields.Str(), attribute="record-bases", data_key="record-bases"
        )
        record_service_bases = ma.fields.List(
            ma.fields.Str(),
            attribute="record-service-bases",
            data_key="record-service-bases",
        )
        record_service_config_bases = ma.fields.List(
            ma.fields.Str(),
            attribute="record-service-config-bases",
            data_key="record-service-config-bases",
        )

        # json schema
        jsonschemas_package = ma.fields.String(
            data_key="jsonschemas-package",
            required=False,
            attribute="jsonschemas-package",
        )
        schema_server = ma.fields.String(
            attribute="schema-server", data_key="schema-server", required=False
        )
        schema_name = ma.fields.String(
            attribute="schema-name", data_key="schema-name", required=False
        )
        schema_version = ma.fields.String(
            attribute="schema-version", data_key="schema-version", required=False
        )
        schema_file = ma.fields.String(
            attribute="schema-file", data_key="schema-file", required=False
        )

        # mapping
        mapping_file = ma.fields.String(
            data_key="mapping-file",
            required=False,
            attribute="mapping-file",
        )
        mapping_package = ma.fields.String(
            data_key="mapping-package",
            required=False,
            attribute="mapping-package",
        )
        index_name = ma.fields.String(
            data_key="index-name", attribute="index-name", required=False
        )

        # marshmallow
        marshmallow = ma.fields.Nested(ModelMarshmallowSchema)

        # ui
        ui = ma.fields.Nested(ModelUISchema)

    def _process_mapping(self, section, **kwargs):
        section["enabled"] = True
        super()._process_mapping(section, **kwargs)
        section.pop("type")
        section.pop("enabled")
        mappings = {k: section.pop(k) for k in list(section)}
        section["mappings"] = mappings
