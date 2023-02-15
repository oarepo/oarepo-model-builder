import pathlib
import re
import typing

import marshmallow as ma
from marshmallow import fields
from marshmallow.error_store import ErrorStore
from marshmallow.exceptions import ValidationError
from marshmallow_oneofschema import OneOfSchema
from marshmallow_union import Union

from .model_validation import model_validator


class PathOrString(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value  # keep the pathlib.Path in here

    def _deserialize(self, value, attr, data, **kwargs):
        if not value:
            return value
        if isinstance(value, pathlib.Path):
            return value
        return value


class ModelDefaults(ma.Schema):
    package = fields.String(required=False)
    profile_package = fields.String(data_key="profile-package", required=False)
    package_path = PathOrString(data_key="package-path")
    jsonschemas_package = fields.String(data_key="jsonschemas-package", required=False)
    mapping_file = fields.String(data_key="mapping-file", required=False)
    collection_url = fields.String(data_key="collection-url", required=False)
    model_name = fields.String(data_key="model-name", required=False)
    schema_name = fields.String(data_key="schema-name", required=False)
    index_name = fields.String(data_key="index-name", required=False)
    script_import_sample_data = fields.String(
        data_key="script-import-sample-data", required=False
    )
    kebap_package = fields.String(data_key="kebap-package", required=False)
    schema_file = fields.String(data_key="schema-file", required=False)
    package_base = fields.String(data_key="package-base", required=False)
    mapping_package = fields.String(data_key="mapping-package", required=False)
    schema_server = fields.String(data_key="schema-server", required=False)
    schema_version = fields.String(data_key="schema-version", required=False)
    package_base_upper = fields.String(data_key="package-base-upper", required=False)
    saved_model_file = PathOrString(data_key="saved-model-file", required=False)
    config_dummy_class = fields.String(data_key="config-dummy-class", required=False)
    config_package = fields.String(data_key="config-package", required=False)
    config_resource_class_key = fields.String(
        data_key="config-resource-class-key", required=False
    )
    config_resource_config_key = fields.String(
        data_key="config-resource-config-key", required=False
    )
    config_service_class_key = fields.String(
        data_key="config-service-class-key", required=False
    )
    config_service_config_key = fields.String(
        data_key="config-service-config-key", required=False
    )
    config_resource_register_blueprint_key = fields.String(
        data_key="config-resource-register-blueprint-key", required=False
    )
    create_blueprint_from_app = fields.String(
        data_key="create-blueprint-from-app", required=False
    )
    ext_class = fields.String(data_key="ext-class", required=False)
    flask_extension_name = fields.String(
        data_key="flask-extension-name", required=False
    )
    cli_function = fields.String(data_key="cli-function", required=False)
    proxies_current_resource = fields.String(
        data_key="proxies-current-resource", required=False
    )
    proxies_current_service = fields.String(
        data_key="proxies-current-service", required=False
    )
    record_class = fields.String(data_key="record-class", required=False)
    record_dumper_class = fields.String(data_key="record-dumper-class", required=False)
    record_facets_class = fields.String(data_key="record-facets-class", required=False)
    record_jsonschemas_setup_cfg = fields.String(
        data_key="record-jsonschemas-setup-cfg", required=False
    )
    record_mapping_setup_cfg = fields.String(
        data_key="record-mapping-setup-cfg", required=False
    )
    record_api_blueprints_setup_cfg = fields.String(
        data_key="record-api-blueprints-setup-cfg", required=False
    )
    record_blueprints_setup_cfg = fields.String(
        data_key="record-blueprints-setup-cfg", required=False
    )
    oarepo_models_setup_cfg = fields.String(
        data_key="oarepo-models-setup-cfg", required=False
    )
    flask_commands_setup_cfg = fields.String(
        data_key="flask-commands-setup-cfg", required=False
    )
    record_metadata_class = fields.String(
        data_key="record-metadata-class", required=False
    )
    record_metadata_table_name = fields.String(
        data_key="record-metadata-table-name", required=False
    )
    record_permissions_class = fields.String(
        data_key="record-permissions-class", required=False
    )
    record_prefix_snake = fields.String(data_key="record-prefix-snake", required=False)
    record_resource_blueprint_name = fields.String(
        data_key="record-resource-blueprint-name", required=False
    )
    record_resource_class = fields.String(
        data_key="record-resource-class", required=False
    )
    record_resource_config_class = fields.String(
        data_key="record-resource-config-class", required=False
    )
    record_schema_class = fields.String(data_key="record-schema-class", required=False)
    record_schema_metadata_alembic = fields.String(
        data_key="record-schema-metadata-alembic", required=False
    )
    record_schema_metadata_class = fields.String(
        data_key="record-schema-metadata-class", required=False
    )
    record_schema_metadata_setup_cfg = fields.String(
        data_key="record-schema-metadata-setup-cfg", required=False
    )
    record_search_options_class = fields.String(
        data_key="record-search-options-class", required=False
    )
    record_service_class = fields.String(
        data_key="record-service-class", required=False
    )
    record_service_config_class = fields.String(
        data_key="record-service-config-class", required=False
    )
    record_prefix = fields.String(data_key="record-prefix", required=False)
    record_records_package = fields.String(
        data_key="record-records-package", required=False
    )
    record_services_package = fields.String(
        data_key="record-services-package", required=False
    )
    record_resources_package = fields.String(
        data_key="record-resources-package", required=False
    )
    config_dummy_bases = fields.List(
        fields.String(), data_key="config-dummy-bases", required=False
    )
    ext_bases = fields.List(fields.String(), data_key="ext-bases", required=False)
    record_facets_bases = fields.List(
        fields.String(), data_key="record-facets-bases", required=False
    )
    record_schema_metadata_bases = fields.List(
        fields.String(), data_key="record-schema-metadata-bases", required=False
    )
    record_bases = fields.List(fields.String(), data_key="record-bases", required=False)
    record_dumper_bases = fields.List(
        fields.String(), data_key="record-dumper-bases", required=False
    )
    record_metadata_bases = fields.List(
        fields.String(), data_key="record-metadata-bases", required=False
    )
    record_permissions_bases = fields.List(
        fields.String(), data_key="record-permissions-bases", required=False
    )
    record_resource_bases = fields.List(
        fields.String(), data_key="record-resource-bases", required=False
    )
    record_resource_config_bases = fields.List(
        fields.String(), data_key="record-resource-config-bases", required=False
    )
    record_schema_bases = fields.List(
        fields.String(), data_key="record-schema-bases", required=False
    )
    record_search_options_bases = fields.List(
        fields.String(), data_key="record-search-options-bases", required=False
    )
    record_service_bases = fields.List(
        fields.String(), data_key="record-service-bases", required=False
    )
    record_service_config_bases = fields.List(
        fields.String(), data_key="record-service-config-bases", required=False
    )
    record_service_config_components = fields.List(
        fields.String(), data_key="record-service-config-components", required=False
    )
    record_dumper_extensions = fields.List(
        fields.String(), data_key="record-dumper-extensions", required=False
    )
    generate_record_pid_field = fields.Boolean(
        data_key="generate-record-pid-field", required=False
    )
    record_service_config_generate_links = fields.Boolean(
        data_key="record-service-config-generate-links", required=False
    )
    invenio_config_extra_code = fields.String(
        data_key="invenio-config-extra-code", required=False
    )
    invenio_ext_extra_code = fields.String(
        data_key="invenio-ext-extra-code", required=False
    )
    invenio_proxies_extra_code = fields.String(
        data_key="invenio-proxies-extra-code", required=False
    )
    invenio_record_extra_code = fields.String(
        data_key="invenio-record-extra-code", required=False
    )
    invenio_record_dumper_extra_code = fields.String(
        data_key="invenio-record-dumper-extra-code", required=False
    )
    invenio_record_facets_extra_code = fields.String(
        data_key="invenio-record-facets-extra-code", required=False
    )
    invenio_record_metadata_extra_code = fields.String(
        data_key="invenio-record-metadata-extra-code", required=False
    )
    invenio_record_object_schema_extra_code = fields.String(
        data_key="invenio-record-object-schema-extra-code", required=False
    )
    invenio_record_permissions_extra_code = fields.String(
        data_key="invenio-record-permissions-extra-code", required=False
    )
    invenio_record_resource_extra_code = fields.String(
        data_key="invenio-record-resource-extra-code", required=False
    )
    invenio_record_resource_config_extra_code = fields.String(
        data_key="invenio-record-resource-config-extra-code", required=False
    )
    invenio_record_schema_extra_code = fields.String(
        data_key="invenio-record-schema-extra-code", required=False
    )
    invenio_record_search_options_extra_code = fields.String(
        data_key="invenio-record-search-options-extra-code", required=False
    )
    invenio_record_service_extra_code = fields.String(
        data_key="invenio-record-service-extra-code", required=False
    )
    invenio_record_service_config_extra_code = fields.String(
        data_key="invenio-record-service-config-extra-code", required=False
    )
    invenio_version_extra_code = fields.String(
        data_key="invenio-version-extra-code", required=False
    )
    invenio_views_extra_code = fields.String(
        data_key="invenio-views-extra-code", required=False
    )
    service_id = fields.String(data_key="service-id", required=False)
    extension_suffix = fields.String(data_key="extension-suffix", required=False)

    mapping = fields.Nested(ma.Schema())
