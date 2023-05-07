from oarepo_model_builder.schema import ModelSchema


def test_prepare_datatype():
    model = ModelSchema(
        "",
        {
            "settings": {
                "python": {
                    "use-isort": False,
                    "use-black": False,
                    "use-autoflake": False,
                },
                "opensearch": {"version": "os-v2"},
            },
            "record": {
                "type": "model",
                "model-name": "My Test Record",
                "module": {"qualified": "my.test"},
                "properties": {"metadata": {"type": "object"}},
            },
        },
    )
    record_section = model.get_schema_section(profile="record", section="record")
    assert record_section.definition == {
        "api-blueprint": {
            "alias": "my_test_record",
            "extra_code": "",
            "function": "my.test.views.records.api.create_blueprint_from_app",
            "generate": True,
            "imports": [],
            "module": "my.test.views.records.api",
        },
        "config": {
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.config",
        },
        "ext": {
            "alias": "my_test_record",
            "base-classes": [],
            "class": "my.test.ext.TestExt",
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.ext",
        },
        "facets": {
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.services.records.facets",
        },
        "json-schema": {
            "alias": "my_test_record",
            "file": "my/test/records/jsonschemas/test-1.0.0.json",
            "generate": True,
            "name": "test-1.0.0.json",
            "version": "1.0.0",
        },
        "mapping": {
            "alias": "my_test_record",
            "file": "my/test/records/mappings/os-v2/test",
            "generate": True,
            "index": "test",
        },
        "marshmallow": {
            "base-classes": ["ma.Schema"],
            "class": "my.test.services.records.schema.TestSchema",
            "extra-code": "",
            "generate": True,
            "module": "my.test.services.records.schema",
        },
        "model-name": "My Test Record",
        "module": {
            "alias": "my_test_record",
            "base": "test",
            "base-upper": "TEST",
            "kebab-module": "my-test",
            "path": "my/test",
            "prefix": "Test",
            "prefix-snake": "test",
            "prefix-upper": "TEST",
            "qualified": "my.test",
            "suffix": "test",
            "suffix-snake": "test",
            "suffix-upper": "TEST",
        },
        "permissions": {
            "base-classes": ["RecordPermissionPolicy"],
            "class": "my.test.services.records.permissions.TestPermissionPolicy",
            "extra-code": "",
            "generate": False,
            "imports": [
                {"import": "invenio_records_permissions.RecordPermissionPolicy"}
            ],
            "module": "my.test.services.records.permissions",
            "presets": [],
        },
        "pid": {
            "context-class": "PIDFieldContext",
            "field-args": ["create=True"],
            "field-class": "PIDField",
            "generate": True,
            "imports": [
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDField"
                },
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
                },
                {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
            ],
            "module": "my.test.records.api",
            "provider-base-classes": ["RecordIdProviderV2"],
            "provider-class": "my.test.records.api.TestIdProvider",
            "type": "mytcrd",
        },
        "properties": {
            "metadata": {
                "marshmallow": {
                    "base-classes": ["ma.Schema"],
                    "class": "my.test.services.records.schema.TestMetadataSchema",
                    "extra-code": "",
                    "generate": True,
                    "module": "my.test.services.records.schema",
                },
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "base-classes": ["ma.Schema"],
                        "class": "my.test.services.records.schema.TestMetadataUISchema",
                        "extra-code": "",
                        "generate": True,
                        "module": "my.test.services.records.schema",
                    }
                },
            }
        },
        "record": {
            "base-classes": ["invenio_records_resources.records.api.Record"],
            "class": "my.test.records.api.TestRecord",
            "extra-code": "",
            "generate": True,
            "imports": [{"import": "invenio_records_resources.records.api.Record"}],
            "module": "my.test.records.api",
        },
        "record-dumper": {
            "base-classes": ["SearchDumper"],
            "class": "my.test.records.records.dumper.TestDumper",
            "extensions": [],
            "extra-code": "",
            "generate": True,
            "imports": [{"import": "invenio_records.dumpers.SearchDumper"}],
            "module": "my.test.records.records",
        },
        "record-metadata": {
            "alembic": "test",
            "alias": "my_test_record",
            "base-classes": ["invenio_records.models.RecordMetadataBase"],
            "class": "my.test.records.models.TestMetadata",
            "extra-code": "",
            "generate": True,
            "module": "my.test.records.models",
            "table": "test_metadata",
        },
        "resource": {
            "base-classes": ["invenio_records_resources.resources.RecordResource"],
            "class": "my.test.resources.records.resource.TestResource",
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResource"}
            ],
            "module": "my.test.resources.records.resource",
            "proxy": "my.test.proxies.current_resource",
        },
        "resource-config": {
            "base-classes": [
                "invenio_records_resources.resources.RecordResourceConfig"
            ],
            "base-url": "/my-test/",
            "class": "my.test.resources.records.config.TestResourceConfig",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResourceConfig"}
            ],
            "module": "my.test.resources.records.config",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "saved-model": {"alias": "my_test_record", "file": "my/test/models/model.json"},
        "search-options": {
            "base-classes": ["InvenioSearchOptions"],
            "class": "my.test.services.records.search.TestSearchOptions",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioSearchOptions",
                    "import": "invenio_records_resources.services.SearchOptions",
                }
            ],
            "module": "my.test.services.records.search",
        },
        "service": {
            "base-classes": ["RecordService"],
            "class": "my.test.services.records.service.TestService",
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [{"import": "invenio_records_resources.services.RecordService"}],
            "module": "my.test.services.records.service",
            "proxy": "my.test.proxies.current_service",
        },
        "service-config": {
            "base-classes": ["RecordServiceConfig"],
            "class": "my.test.services.records.config.TestServiceConfig",
            "components": [],
            "config-key": "TEST_RECORD_SERVICE_CONFIG",
            "extra-code": "",
            "generate": True,
            "generate-links": True,
            "imports": [
                {"import": "invenio_records_resources.services.RecordServiceConfig"}
            ],
            "module": "my.test.services.records.config",
            "service-id": "my_test_record",
        },
        "type": "model",
        "ui": {
            "marshmallow": {
                "base-classes": ["InvenioUISchema"],
                "class": "my.test.services.records.schema.TestUISchema",
                "extra-code": "",
                "generate": True,
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
                "module": "my.test.services.records.schema",
            }
        },
        "ui-blueprint": {
            "alias": "my_test_record",
            "extra_code": "",
            "function": "my.test.views.records.ui.create_blueprint_from_app",
            "generate": True,
            "imports": [],
            "module": "my.test.views.records.ui",
        },
    }