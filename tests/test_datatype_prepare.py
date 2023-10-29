from oarepo_model_builder.schema import ModelSchema


def test_prepare_datatype():
    module = "my.test"
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
                "module": {"qualified": f"{module}"},
                "properties": {"metadata": {"type": "object"}},
            },
        },
    )
    record_section = model.get_schema_section(profile="record", section="record")
    assert record_section.definition == {
        "api-blueprint": {
            "alias": "my_test_record",
            "extra_code": "",
            "function": "my.test.views.records.api.create_api_blueprint",
            "generate": True,
            "imports": [],
            "module": "my.test.views.records.api",
        },
        "app-blueprint": {
            "alias": "my_test_record",
            "extra_code": "",
            "function": "my.test.views.records.app.create_app_blueprint",
            "generate": True,
            "imports": [],
            "module": "my.test.views.records.app",
        },
        "config": {
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.config",
        },
        "ext": {
            "alias": "my.test",
            "base-classes": [],
            "class": "my.test.ext.TestExt",
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.ext",
        },
        "ext-resource": {"generate": True, "skip": False},
        "facets": {
            "extra-code": "",
            "generate": True,
            "module": "my.test.services.records.facets",
        },
        "json-schema-settings": {
            "alias": "my_test_record",
            "file": "my/test/records/jsonschemas/test-1.0.0.json",
            "generate": True,
            "module": "my.test.records.jsonschemas",
            "name": "test-1.0.0.json",
            "version": "1.0.0",
        },
        "json-serializer": {
            "base-classes": ["oarepo_runtime.resources.LocalizedUIJSONSerializer"],
            "class": "my.test.resources.records.ui.TestUIJSONSerializer",
            "extra-code": "",
            "format_serializer_cls": "flask_resources.serializers.JSONSerializer",
            "generate": True,
            "imports": [],
            "list_schema_cls": "flask_resources.BaseListSchema",
            "module": "my.test.resources.records.ui",
        },
        "mapping": {
            "alias": "my_test_record",
            "file": "my/test/records/mappings/os-v2/my_test_record/test-1.0.0.json",
            "generate": True,
            "index": "my_test_record-test-1.0.0",
            "module": "my.test.records.mappings",
        },
        "marshmallow": {
            "base-classes": ["marshmallow.Schema"],
            "class": "my.test.services.records.schema.TestSchema",
            "extra-code": "",
            "generate": True,
            "module": "my.test.services.records.schema",
        },
        "model-name": "My Test Record",
        "module": {
            "alias": "my_test_record",
            "base": "test",
            "base-title": "Test",
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
            "base-classes": ["invenio_records_permissions.RecordPermissionPolicy"],
            "class": "my.test.services.records.permissions.TestPermissionPolicy",
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.services.records.permissions",
            "presets": ["everyone"],
        },
        "pid": {
            "context-class": "invenio_records_resources.records.systemfields.pid.PIDFieldContext",
            "extra-code": "",
            "field-args": ["create=True"],
            "field-class": "invenio_records_resources.records.systemfields.pid.PIDField",
            "generate": True,
            "imports": [],
            "module": "my.test.records.api",
            "provider-base-classes": [
                "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"
            ],
            "provider-class": "my.test.records.api.TestIdProvider",
            "type": "mytcrd",
        },
        "properties": {
            "metadata": {
                "marshmallow": {
                    "base-classes": ["marshmallow.Schema"],
                    "class": "my.test.services.records.schema.TestMetadataSchema",
                    "extra-code": "",
                    "generate": True,
                    "module": "my.test.services.records.schema",
                },
                "properties": {},
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "base-classes": ["marshmallow.Schema"],
                        "class": "my.test.services.records.ui_schema.TestMetadataUISchema",
                        "extra-code": "",
                        "generate": True,
                        "module": "my.test.services.records.ui_schema",
                    }
                },
            }
        },
        "proxy": {"generate": True, "module": "my.test.proxies"},
        "record": {
            "base-classes": [
                "invenio_records_resources.records.api.Record{InvenioRecord}"
            ],
            "class": "my.test.records.api.TestRecord",
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.records.api",
        },
        "record-dumper": {
            "base-classes": ["oarepo_runtime.records.dumpers.SearchDumper"],
            "class": "my.test.records.dumpers.dumper.TestDumper",
            "extensions": [
                "{{my.test.records.dumpers.edtf.TestEDTFIntervalDumperExt}}()"
            ],
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.records.dumpers.dumper",
        },
        "edtf-interval-dumper": {
            "base-classes": [
                "oarepo_runtime.records.dumpers.edtf_interval.EDTFIntervalDumperExt"
            ],
            "class": "my.test.records.dumpers.edtf.TestEDTFIntervalDumperExt",
            "extensions": [],
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.records.dumpers.edtf",
        },
        "record-metadata": {
            "alembic": "my.test.alembic",
            "alias": "my_test_record",
            "base-classes": [
                "invenio_db.db{db.Model}",
                "invenio_records.models.RecordMetadataBase",
            ],
            "class": "my.test.records.models.TestMetadata",
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.records.models",
            "table": "test_metadata",
            "use-versioning": True,
        },
        "resource": {
            "base-classes": ["invenio_records_resources.resources.RecordResource"],
            "class": "my.test.resources.records.resource.TestResource",
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.resources.records.resource",
            "proxy": "current_resource",
        },
        "resource-config": {
            "base-classes": [
                "invenio_records_resources.resources.RecordResourceConfig"
            ],
            "base-html-url": "/my-test/",
            "base-url": "/my-test/",
            "class": "my.test.resources.records.config.TestResourceConfig",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.resources.records.config",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "saved-model": {
            "alias": "my_test_record",
            "file": "my/test/models/records.json",
            "module": "my.test.models",
        },
        "search-options": {
            "base-classes": [
                "invenio_records_resources.services.SearchOptions{InvenioSearchOptions}"
            ],
            "class": "my.test.services.records.search.TestSearchOptions",
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.services.records.search",
            "sort-options-field": "sort_options",
        },
        "searchable": True,
        "service": {
            "base-classes": [
                "invenio_records_resources.services.RecordService{InvenioRecordService}"
            ],
            "class": "my.test.services.records.service.TestService",
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [],
            "module": "my.test.services.records.service",
            "proxy": "current_service",
        },
        "service-config": {
            "base-classes": [
                "oarepo_runtime.config.service.PermissionsPresetsConfigMixin",
                "invenio_records_resources.services.RecordServiceConfig{InvenioRecordServiceConfig}",
            ],
            "class": "my.test.services.records.config.TestServiceConfig",
            "components": [],
            "config-key": "TEST_RECORD_SERVICE_CONFIG",
            "extra-code": "",
            "generate": True,
            "module": "my.test.services.records.config",
            "service-id": "test",
        },
        "sortable": [],
        "type": "model",
        "ui": {
            "marshmallow": {
                "base-classes": ["oarepo_runtime.services.schema.ui.InvenioUISchema"],
                "class": "my.test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
                "generate": True,
                "imports": [],
                "module": "my.test.services.records.ui_schema",
            }
        },
    }


def test_ids():
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
                "properties": {
                    "a": {"type": "integer", "id": "_a"},
                    "b": {
                        "type": "object",
                        "properties": {
                            "c": {"type": "integer", "id": "_c"},
                            "d": {
                                "type": "array",
                                "id": "_d",
                                "items": {
                                    "type": "object",
                                    "id": "_di",
                                    "properties": {
                                        "e": {"type": "integer", "id": "_e"},
                                    },
                                },
                            },
                        },
                        "id": "_b",
                    },
                },
            },
        },
    )
    dt = model.get_schema_section("record", "record")
    assert dt.id is None
    assert dt.children["a"].id == "_a"
    assert dt.children["b"].id == "_b"
    assert dt.children["b"].children["c"].id == "_c"
    assert dt.children["b"].children["d"].id == "_d"
    assert dt.children["b"].children["d"].item.id == "_di"
    assert dt.children["b"].children["d"].item.children["e"].id == "_e"
