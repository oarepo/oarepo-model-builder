import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import ImportSchema


class ModelPermissionsSchema(ma.Schema):
    presets = ma.fields.List(ma.fields.String())

    class Meta:
        unknown = ma.RAISE


class InvenioModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        oarepo_models_setup_cfg = ma.fields.String(
            attribute="oarepo-models-setup-cfg",
            data_key="oarepo-models-setup-cfg",
            required=False,
        )
        record_prefix = ma.fields.String(
            attribute="record-prefix", data_key="record-prefix", required=False
        )

        config_package = ma.fields.String(
            attribute="config-package", data_key="config-package"
        )
        permissions = ma.fields.Nested(ModelPermissionsSchema(), required=False)
        record_resource_blueprint_name = ma.fields.String(
            attribute="record-resource-blueprint-name",
            data_key="record-resource-blueprint-name",
        )
        record_mapping_setup_cfg = ma.fields.String(
            attribute="record-mapping-setup-cfg", data_key="record-mapping-setup-cfg"
        )
        invenio_proxies_extra_code = ma.fields.String(
            attribute="invenio-proxies-extra-code",
            data_key="invenio-proxies-extra-code",
        )
        record_resources_package = ma.fields.String(
            attribute="record-resources-package", data_key="record-resources-package"
        )
        proxies_current_service = ma.fields.String(
            attribute="proxies-current-service", data_key="proxies-current-service"
        )
        record_class = ma.fields.String(
            attribute="record-class", data_key="record-class"
        )
        config_dummy_class = ma.fields.String(
            attribute="config-dummy-class", data_key="config-dummy-class"
        )
        invenio_version_extra_code = ma.fields.String(
            attribute="invenio-version-extra-code",
            data_key="invenio-version-extra-code",
        )
        record_schema_metadata_class = ma.fields.String(
            attribute="record-schema-metadata-class",
            data_key="record-schema-metadata-class",
        )
        config_resource_config_key = ma.fields.String(
            attribute="config-resource-config-key",
            data_key="config-resource-config-key",
        )
        pid_type = ma.fields.String(attribute="pid-type", data_key="pid-type")
        record_resource_class = ma.fields.String(
            attribute="record-resource-class", data_key="record-resource-class"
        )
        invenio_record_service_extra_code = ma.fields.String(
            attribute="invenio-record-service-extra-code",
            data_key="invenio-record-service-extra-code",
        )
        record_jsonschemas_setup_cfg = ma.fields.String(
            attribute="record-jsonschemas-setup-cfg",
            data_key="record-jsonschemas-setup-cfg",
        )
        record_service_config_components = ma.fields.List(
            ma.fields.String(),
            attribute="record-service-config-components",
            data_key="record-service-config-components",
        )
        create_blueprint_from_app = ma.fields.String(
            attribute="create-blueprint-from-app", data_key="create-blueprint-from-app"
        )
        flask_extension_name = ma.fields.String(
            attribute="flask-extension-name", data_key="flask-extension-name"
        )
        record_permissions_class = ma.fields.String(
            attribute="record-permissions-class", data_key="record-permissions-class"
        )
        invenio_record_metadata_extra_code = ma.fields.String(
            attribute="invenio-record-metadata-extra-code",
            data_key="invenio-record-metadata-extra-code",
        )
        pid_field_imports = ma.fields.List(
            ma.fields.Nested(ImportSchema),
            attribute="pid-field-imports",
            data_key="pid-field-imports",
        )
        record_api_blueprints_setup_cfg = ma.fields.String(
            attribute="record-api-blueprints-setup-cfg",
            data_key="record-api-blueprints-setup-cfg",
        )
        record_schema_metadata_alembic = ma.fields.String(
            attribute="record-schema-metadata-alembic",
            data_key="record-schema-metadata-alembic",
        )
        flask_commands_setup_cfg = ma.fields.String(
            attribute="flask-commands-setup-cfg", data_key="flask-commands-setup-cfg"
        )
        invenio_record_service_config_extra_code = ma.fields.String(
            attribute="invenio-record-service-config-extra-code",
            data_key="invenio-record-service-config-extra-code",
        )
        record_metadata_class = ma.fields.String(
            attribute="record-metadata-class", data_key="record-metadata-class"
        )
        record_service_class = ma.fields.String(
            attribute="record-service-class", data_key="record-service-class"
        )
        pid_field_provider = ma.fields.String(
            attribute="pid-field-provider", data_key="pid-field-provider"
        )
        invenio_record_resource_config_extra_code = ma.fields.String(
            attribute="invenio-record-resource-config-extra-code",
            data_key="invenio-record-resource-config-extra-code",
        )
        record_pid_provider_class = ma.fields.String(
            attribute="record-pid-provider-class", data_key="record-pid-provider-class"
        )
        config_service_config_key = ma.fields.String(
            attribute="config-service-config-key", data_key="config-service-config-key"
        )
        pid_field_args = ma.fields.List(
            ma.fields.String(), attribute="pid-field-args", data_key="pid-field-args"
        )
        record_service_config_class = ma.fields.String(
            attribute="record-service-config-class",
            data_key="record-service-config-class",
        )
        record_metadata_table_name = ma.fields.String(
            attribute="record-metadata-table-name",
            data_key="record-metadata-table-name",
        )
        cli_function = ma.fields.String(
            attribute="cli-function", data_key="cli-function"
        )
        invenio_config_extra_code = ma.fields.String(
            attribute="invenio-config-extra-code", data_key="invenio-config-extra-code"
        )
        pid_field_cls = ma.fields.String(
            attribute="pid-field-cls", data_key="pid-field-cls"
        )
        record_services_package = ma.fields.String(
            attribute="record-services-package", data_key="record-services-package"
        )
        invenio_record_permissions_extra_code = ma.fields.String(
            attribute="invenio-record-permissions-extra-code",
            data_key="invenio-record-permissions-extra-code",
        )
        invenio_views_extra_code = ma.fields.String(
            attribute="invenio-views-extra-code", data_key="invenio-views-extra-code"
        )
        generate_record_pid_field = ma.fields.Bool(
            attribute="generate-record-pid-field", data_key="generate-record-pid-field"
        )
        record_search_options_class = ma.fields.String(
            attribute="record-search-options-class",
            data_key="record-search-options-class",
        )
        extension_suffix = ma.fields.String(
            attribute="extension-suffix", data_key="extension-suffix"
        )
        config_resource_class_key = ma.fields.String(
            attribute="config-resource-class-key", data_key="config-resource-class-key"
        )
        config_service_class_key = ma.fields.String(
            attribute="config-service-class-key", data_key="config-service-class-key"
        )
        proxies_current_resource = ma.fields.String(
            attribute="proxies-current-resource", data_key="proxies-current-resource"
        )
        record_dumper_extensions = ma.fields.List(
            ma.fields.String(),
            attribute="record-dumper-extensions",
            data_key="record-dumper-extensions",
        )
        record_ui_schema_metadata_class = ma.fields.String(
            attribute="record-ui-schema-metadata-class",
            data_key="record-ui-schema-metadata-class",
        )
        invenio_record_search_options_extra_code = ma.fields.String(
            attribute="invenio-record-search-options-extra-code",
            data_key="invenio-record-search-options-extra-code",
        )
        record_prefix_snake = ma.fields.String(
            attribute="record-prefix-snake", data_key="record-prefix-snake"
        )
        record_schema_metadata_setup_cfg = ma.fields.String(
            attribute="record-schema-metadata-setup-cfg",
            data_key="record-schema-metadata-setup-cfg",
        )
        invenio_record_resource_extra_code = ma.fields.String(
            attribute="invenio-record-resource-extra-code",
            data_key="invenio-record-resource-extra-code",
        )
        record_ui_schema_class = ma.fields.String(
            attribute="record-ui-schema-class", data_key="record-ui-schema-class"
        )
        script_import_sample_data = ma.fields.String(
            attribute="script-import-sample-data", data_key="script-import-sample-data"
        )
        record_blueprints_setup_cfg = ma.fields.String(
            attribute="record-blueprints-setup-cfg",
            data_key="record-blueprints-setup-cfg",
        )
        ext_class = ma.fields.String(attribute="ext-class", data_key="ext-class")
        invenio_record_schema_extra_code = ma.fields.String(
            attribute="invenio-record-schema-extra-code",
            data_key="invenio-record-schema-extra-code",
        )
        config_resource_register_blueprint_key = ma.fields.String(
            attribute="config-resource-register-blueprint-key",
            data_key="config-resource-register-blueprint-key",
        )
        record_resource_config_class = ma.fields.String(
            attribute="record-resource-config-class",
            data_key="record-resource-config-class",
        )
        invenio_record_dumper_extra_code = ma.fields.String(
            attribute="invenio-record-dumper-extra-code",
            data_key="invenio-record-dumper-extra-code",
        )
        invenio_ext_extra_code = ma.fields.String(
            attribute="invenio-ext-extra-code", data_key="invenio-ext-extra-code"
        )
        service_id = ma.fields.String(attribute="service-id", data_key="service-id")
        record_dumper_class = ma.fields.String(
            attribute="record-dumper-class", data_key="record-dumper-class"
        )
        record_records_package = ma.fields.String(
            attribute="record-records-package", data_key="record-records-package"
        )
        invenio_record_facets_extra_code = ma.fields.String(
            attribute="invenio-record-facets-extra-code",
            data_key="invenio-record-facets-extra-code",
        )
        record_ui_serializer_class = ma.fields.String(
            attribute="record-ui-serializer-class",
            data_key="record-ui-serializer-class",
        )
        invenio_record_extra_code = ma.fields.String(
            attribute="invenio-record-extra-code", data_key="invenio-record-extra-code"
        )
        record_service_config_generate_links = ma.fields.Bool(
            attribute="record-service-config-generate-links",
            data_key="record-service-config-generate-links",
        )
        pid_field_context = ma.fields.String(
            attribute="pid-field-context", data_key="pid-field-context"
        )
        invenio_record_object_schema_extra_code = ma.fields.String(
            attribute="invenio-record-object-schema-extra-code",
            data_key="invenio-record-object-schema-extra-code",
        )
        record_schema_class = ma.fields.String(
            attribute="record-schema-class", data_key="record-schema-class"
        )
        record_facets_class = ma.fields.String(
            attribute="record-facets-class", data_key="record-facets-class"
        )
