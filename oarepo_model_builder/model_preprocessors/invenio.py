from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case, snake_case
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.jinja import split_base_name


class InvenioModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio"

    def transform(self, schema, settings):
        model = schema.current_model
        deepmerge(settings, {"python": {"templates": {}}})
        deepmerge(
            model,
            {
                # just make sure that the templates is always there
                "marshmallow": {},
            },
        )

        record_prefix = model.record_prefix

        extension_suffix = snake_case(record_prefix)
        extension_suffix_upper = extension_suffix.upper()
        self.set(model, "extension-suffix", lambda: extension_suffix)
        self.set(model, "profile-package", lambda: "records")

        # self.set(model, "extension-suffix", lambda: f"_{record_prefix}")

        self.set(
            model,
            "record-prefix-snake",
            lambda: snake_case(model.record_prefix),
        )

        # level-1 packages

        self.set(
            model,
            "record-resources-package",
            lambda: f"{model.package}.resources.{model.profile_package}",
        )

        self.set(
            model,
            "record-services-package",
            lambda: f"{model.package}.services.{model.profile_package}",
        )

        self.set(
            model,
            "record-records-package",
            lambda: f"{model.package}.{model.profile_package}",
        )

        # config
        self.set(model, "config-package", lambda: f"{model.package}.config")
        self.set(
            model,
            "config-dummy-class",
            lambda: f"{model.package}.config.DummyClass",
        )
        # todo "config prefix"
        self.set(
            model,
            "config-resource-config-key",
            lambda: f"{model.package_base_upper}_RESOURCE_CONFIG_{extension_suffix_upper}",
        )
        self.set(
            model,
            "config-resource-class-key",
            lambda: f"{model.package_base_upper}_RESOURCE_CLASS_{extension_suffix_upper}",
        )
        self.set(
            model,
            "config-service-config-key",
            lambda: f"{model.package_base_upper}_SERVICE_CONFIG_{extension_suffix_upper}",
        )
        self.set(
            model,
            "config-service-class-key",
            lambda: f"{model.package_base_upper}_SERVICE_CLASS_{extension_suffix_upper}",
        )
        self.set(
            model,
            "config-resource-register-blueprint-key",
            lambda: f"{model.package_base_upper}_REGISTER_BLUEPRINT",
        )

        # ext
        self.set(
            model,
            "ext-class",
            lambda: f"{model.package}.ext.{record_prefix}Ext",
        )
        self.set(model, "flask-extension-name", lambda: extension_suffix)

        # cli
        self.set(
            model,
            "cli-function",
            lambda: f"{model.package}.cli.group",
        )

        # proxies
        self.set(
            model,
            "proxies-current-resource",
            lambda: f"{model.package}.proxies.current_resource",
        )
        self.set(
            model,
            "proxies-current-service",
            lambda: f"{model.package}.proxies.current_service",
        )

        # record
        self.set(
            model,
            "record-class",
            lambda: f"{model.record_records_package}.api.{record_prefix}Record",
        )
        self.set(
            model,
            "record-metadata-class",
            lambda: f"{model.record_records_package}.models.{record_prefix}Metadata",
        )
        self.set(
            model,
            "record-metadata-table-name",
            lambda: f"{record_prefix.lower()}_metadata",
        )
        #   - setup.cfg
        self.set(
            model,
            "record-mapping-setup-cfg",
            lambda: f"{extension_suffix}",
        )
        self.set(
            model,
            "record-jsonschemas-setup-cfg",
            lambda: f"{extension_suffix}",
        )
        self.set(
            model,
            "record-api-blueprints-setup-cfg",
            lambda: f"{extension_suffix}",
        )
        self.set(
            model,
            "record-blueprints-setup-cfg",
            lambda: f"{extension_suffix}",
        )

        # resource
        self.set(
            model,
            "record-resource-config-class",
            lambda: f"{model.record_resources_package}.config.{record_prefix}ResourceConfig",
        )
        self.set(
            model,
            "record-resource-class",
            lambda: f"{model.record_resources_package}.resource.{record_prefix}Resource",
        )
        self.set(
            model,
            "record-permissions-class",
            lambda: f"{model.record_services_package}.permissions.{record_prefix}PermissionPolicy",
        )

        # service
        self.set(
            model,
            "record-service-class",
            lambda: f"{model.record_services_package}.service.{record_prefix}Service",
        )
        self.set(
            model,
            "record-service-config-class",
            lambda: f"{model.record_services_package}.config.{record_prefix}ServiceConfig",
        )

        model.setdefault("record-service-config-generate-links", True)
        #   - schema
        self.set(
            model,
            "record-schema-class",
            lambda: f"{model.record_services_package}.schema.{record_prefix}Schema",
        )
        self.set(
            model,
            "record-schema-metadata-class",
            lambda: f"{model.record_services_package}.schema.{record_prefix}MetadataSchema",
        )
        #   - dumper
        self.set(
            model,
            "record-dumper-class",
            lambda: f"{model.record_records_package}.dumper.{record_prefix}Dumper",
        )
        #   - search

        self.set(
            model,
            "record-search-options-class",
            lambda: f"{model.record_services_package}.search.{record_prefix}SearchOptions",
        )

        #   - facets
        self.set(
            model,
            "record-facets-class",
            lambda: f"{model.record_services_package}.facets.Test",
        )

        # alembic
        self.set(
            model,
            "record-schema-metadata-alembic",
            lambda: f"{extension_suffix}",
        )
        self.set(
            model,
            "record-schema-metadata-setup-cfg",
            lambda: f"{extension_suffix}",
        )

        self.set(
            model,
            "flask-commands-setup-cfg",
            lambda: f"{extension_suffix}",
        )

        self.set(model, "record-resource-blueprint-name", lambda: record_prefix)
        self.set(
            model,
            "create-blueprint-from-app",
            lambda: f"{model.package}.views.create_blueprint_from_app_{extension_suffix}",
        )
        model.setdefault("invenio-config-extra-code", "")
        model.setdefault("invenio-ext-extra-code", "")
        model.setdefault("invenio-proxies-extra-code", "")
        model.setdefault("invenio-record-extra-code", "")
        model.setdefault("invenio-record-dumper-extra-code", "")
        model.setdefault("invenio-record-facets-extra-code", "")
        model.setdefault("invenio-record-metadata-extra-code", "")
        model.setdefault("invenio-record-object-schema-extra-code", "")
        model.setdefault("invenio-record-permissions-extra-code", "")
        model.setdefault("invenio-record-resource-extra-code", "")
        model.setdefault("invenio-record-resource-config-extra-code", "")
        model.setdefault("invenio-record-schema-extra-code", "")
        model.setdefault("invenio-record-search-options-extra-code", "")
        model.setdefault("invenio-record-service-extra-code", "")
        model.setdefault("invenio-record-service-config-extra-code", "")
        model.setdefault("invenio-version-extra-code", "")
        model.setdefault("invenio-views-extra-code", "")

        if schema.model_field in schema.schema:
            current_model_field = schema.schema[schema.model_field]
            schema_class = model.record_schema_class
            schema_metadata_class = model.record_schema_metadata_class
            schema_class_base_classes = model.get(
                "record_schema_metadata_bases", []
            ) + [
                "ma.Schema"  # alias will be recognized automatically
            ]

            if (
                "properties" in current_model_field
                and "metadata" in current_model_field.properties
            ):
                if current_model_field.properties.metadata.get("type") == "object":
                    deepmerge(
                        current_model_field.properties.metadata.setdefault(
                            "marshmallow", {}
                        ),
                        {
                            "schema-class": schema_metadata_class,
                            "base-classes": schema_class_base_classes,
                            "generate": True,
                        },
                    )
            if (
                "marshmallow" in schema.schema
                and "base-schema" in schema.schema["marshmallow"]
            ):
                schema_class_base_classes = model.get(
                    "record_schema_metadata_bases", []
                ) + [
                    schema.schema["marshmallow"][
                        "base_schema"
                    ]  # alias will be recognized automatically
                ]

            deepmerge(
                current_model_field.setdefault("marshmallow", {}),
                {
                    "schema-class": schema_class,
                    "base-classes": schema_class_base_classes,
                    "generate": True,
                },
            )
            current_model_field.setdefault("type", "object")

        model.setdefault("generate-record-pid-field", True)
        model.setdefault("record-dumper-extensions", [])

        # default import prefixes
        _prefixes = settings.python.setdefault("always-defined-import-prefixes", [])
        for _prefix in ["ma", "ma_fields", "ma_valid"]:
            if _prefix not in _prefixes:
                _prefixes.append(_prefix)

        model.setdefault("script-import-sample-data", "data/sample_data.yaml")
        self.set(model, "service-id", lambda: model.flask_extension_name)
