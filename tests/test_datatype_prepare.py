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
        "type": "model",
        "properties": {
            "metadata": {
                "type": "object",
                "properties": {},
                "marshmallow": {
                    "module": "my.test.services.records.schema",
                    "generate": True,
                    "class": "my.test.services.records.schema.TestMetadataSchema",
                    "extra-code": "",
                    "base-classes": ["marshmallow.Schema"],
                },
                "ui": {
                    "marshmallow": {
                        "generate": True,
                        "module": "my.test.services.records.ui_schema",
                        "class": "my.test.services.records.ui_schema.TestMetadataUISchema",
                        "extra-code": "",
                        "base-classes": ["marshmallow.Schema"],
                    }
                },
            }
        },
        "searchable": True,
        "model-name": "My Test Record",
        "module": {
            "qualified": "my.test",
            "alias": "my_test_record",
            "path": "my/test",
            "base": "test",
            "base-upper": "TEST",
            "base-title": "Test",
            "kebab-module": "my-test",
            "prefix": "Test",
            "prefix-upper": "TEST",
            "prefix-snake": "test",
            "suffix": "test",
            "suffix-upper": "TEST",
            "suffix-snake": "test",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "ext-resource": {"generate": True, "service-kwargs": {}, "skip": False},
        "search-options": {
            "generate": True,
            "module": "my.test.services.records.search",
            "extra-code": "",
            "class": "my.test.services.records.search.TestSearchOptions",
            "base-classes": [
                "invenio_records_resources.services.SearchOptions{InvenioSearchOptions}"
            ],
            "imports": [],
            "fields": {},
            "sort-options-field": "sort_options",
        },
        "config": {
            "generate": True,
            "module": "my.test.config",
            "extra_code": "",
            "imports": [],
        },
        "ext": {
            "generate": True,
            "module": "my.test.ext",
            "class": "my.test.ext.TestExt",
            "base-classes": [],
            "extra_code": "",
            "alias": "my.test",
            "imports": [],
        },
        "api-blueprint": {
            "generate": True,
            "alias": "my_test_record",
            "extra_code": "",
            "module": "my.test.views.records.api",
            "function": "my.test.views.records.api.create_api_blueprint",
            "imports": [],
        },
        "app-blueprint": {
            "generate": True,
            "alias": "my_test_record",
            "extra_code": "",
            "module": "my.test.views.records.app",
            "function": "my.test.views.records.app.create_app_blueprint",
            "imports": [],
        },
        "facets": {
            "generate": True,
            "module": "my.test.services.records.facets",
            "groups": True,
            "extra-code": "",
        },
        "record": {
            "generate": True,
            "module": "my.test.records.api",
            "class": "my.test.records.api.TestRecord",
            "base-classes": [
                "invenio_records_resources.records.api.Record{InvenioRecord}"
            ],
            "imports": [],
            "extra-code": "",
            "fields": {},
        },
        "resource": {
            "generate": True,
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "module": "my.test.resources.records.resource",
            "class": "my.test.resources.records.resource.TestResource",
            "proxy": "current_resource",
            "extra-code": "",
            "base-classes": ["invenio_records_resources.resources.RecordResource"],
            "additional-args": [],
            "imports": [],
        },
        "resource-config": {
            "generate": True,
            "base-url": "/my-test/",
            "base-html-url": "/my-test/",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "module": "my.test.resources.records.config",
            "class": "my.test.resources.records.config.TestResourceConfig",
            "extra-code": "",
            "base-classes": [
                "invenio_records_resources.resources.RecordResourceConfig"
            ],
            "additional-args": [],
            "imports": [],
        },
        "saved-model": {
            "file": "my/test/models/records.json",
            "module": "my.test.models",
            "alias": "my_test_record",
        },
        "proxy": {"module": "my.test.proxies", "generate": True},
        "json-schema-settings": {
            "generate": True,
            "alias": "my_test_record",
            "version": "1.0.0",
            "module": "my.test.records.jsonschemas",
            "name": "test-1.0.0.json",
            "file": "my/test/records/jsonschemas/test-1.0.0.json",
        },
        "pid": {
            "generate": True,
            "type": "mytcrd",
            "module": "my.test.records.api",
            "provider-class": "my.test.records.api.TestIdProvider",
            "provider-base-classes": [
                "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"
            ],
            "field-class": "invenio_records_resources.records.systemfields.pid.PIDField",
            "context-class": "invenio_records_resources.records.systemfields.pid.PIDFieldContext",
            "field-args": ["create=True"],
            "imports": [],
            "extra-code": "",
        },
        "record-dumper": {
            "generate": True,
            "module": "my.test.records.dumpers.dumper",
            "class": "my.test.records.dumpers.dumper.TestDumper",
            "base-classes": ["oarepo_runtime.records.dumpers.SearchDumper"],
            "extra-code": "",
            "extensions": [
                "{{my.test.records.dumpers.edtf.TestEDTFIntervalDumperExt}}()"
            ],
            "imports": [],
        },
        "record-metadata": {
            "generate": True,
            "module": "my.test.records.models",
            "class": "my.test.records.models.TestMetadata",
            "base-classes": [
                "invenio_db.db{db.Model}",
                "invenio_records.models.RecordMetadataBase",
            ],
            "extra-code": "",
            "imports": [],
            "table": "test_metadata",
            "alias": "my_test_record",
            "use-versioning": True,
            "alembic": "my.test.alembic",
        },
        "service-config": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CONFIG",
            "module": "my.test.services.records.config",
            "class": "my.test.services.records.config.TestServiceConfig",
            "extra-code": "",
            "service-id": "test",
            "base-classes": [
                "oarepo_runtime.services.config.service.PermissionsPresetsConfigMixin",
                "invenio_records_resources.services.RecordServiceConfig{InvenioRecordServiceConfig}",
            ],
            "search-item-links-template-cls": "invenio_records_resources.services.LinksTemplate",
            "additional-args": [],
            "components": [],
        },
        "service": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "proxy": "current_service",
            "module": "my.test.services.records.service",
            "class": "my.test.services.records.service.TestService",
            "extra-code": "",
            "base-classes": [
                "invenio_records_resources.services.RecordService{InvenioRecordService}"
            ],
            "additional-args": [],
            "imports": [],
        },
        "ui": {
            "marshmallow": {
                "generate": True,
                "module": "my.test.services.records.ui_schema",
                "class": "my.test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
                "base-classes": ["oarepo_runtime.services.schema.ui.InvenioUISchema"],
                "imports": [],
            }
        },
        "json-serializer": {
            "module": "my.test.resources.records.ui",
            "class": "my.test.resources.records.ui.TestUIJSONSerializer",
            "base-classes": ["oarepo_runtime.resources.LocalizedUIJSONSerializer"],
            "imports": [],
            "extra-code": "",
            "generate": True,
            "list_schema_cls": "flask_resources.BaseListSchema",
            "format_serializer_cls": "flask_resources.serializers.JSONSerializer",
            "schema-context-args": {
                '"object_key"': '"ui"',
                '"identity"': "{{ flask.g{g.identity} }}",
            },
        },
        "mapping": {
            "generate": True,
            "alias": "my_test_record",
            "module": "my.test.records.mappings",
            "index": "my_test_record-test-1.0.0",
            "file": "my/test/records/mappings/os-v2/my_test_record/test-1.0.0.json",
            "index-field-args": [],
        },
        "marshmallow": {
            "generate": True,
            "module": "my.test.services.records.schema",
            "class": "my.test.services.records.schema.TestSchema",
            "extra-code": "",
            "base-classes": ["marshmallow.Schema"],
        },
        "permissions": {
            "generate": True,
            "presets": ["everyone"],
            "extra-code": "",
            "module": "my.test.services.records.permissions",
            "class": "my.test.services.records.permissions.TestPermissionPolicy",
            "base-classes": ["invenio_records_permissions.RecordPermissionPolicy"],
            "imports": [],
        },
        "edtf-interval-dumper": {
            "generate": True,
            "module": "my.test.records.dumpers.edtf",
            "class": "my.test.records.dumpers.edtf.TestEDTFIntervalDumperExt",
            "base-classes": [
                "oarepo_runtime.records.dumpers.edtf_interval.EDTFIntervalDumperExt"
            ],
            "extra-code": "",
            "extensions": [],
            "imports": [],
        },
        "record-list": {
            "generate": True,
            "module": "my.test.services.records.results",
            "class": "my.test.services.records.results.TestRecordList",
            "extra-code": "",
            "base-classes": ["oarepo_runtime.services.results.RecordList"],
            "components": [],
            "imports": [],
        },
        "record-item": {
            "generate": True,
            "module": "my.test.services.records.results",
            "class": "my.test.services.records.results.TestRecordItem",
            "extra-code": "",
            "base-classes": ["oarepo_runtime.services.results.RecordItem"],
            "components": [],
            "imports": [],
        },
        "sortable": [],
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
