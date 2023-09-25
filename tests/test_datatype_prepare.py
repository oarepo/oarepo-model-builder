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
            "function": f"{module}.views.records.api.create_api_blueprint",
            "generate": True,
            "imports": [],
            "module": f"{module}.views.records.api",
        },
        "config": {
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": f"{module}.config",
        },
        "ext": {
            "alias": f"{module}",
            "base-classes": [],
            "class": f"{module}.ext.TestExt",
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": f"{module}.ext",
        },
        "ext-resource": {
            "generate": True,
            "skip": False,
        },
        "facets": {
            "extra-code": "",
            "generate": True,
            "module": f"{module}.services.records.facets",
        },
        "json-schema-settings": {
            "alias": "my_test_record",
            "file": "my/test/records/jsonschemas/test-1.0.0.json",
            "generate": True,
            "module": f"{module}.records.jsonschemas",
            "name": "test-1.0.0.json",
            "version": "1.0.0",
        },
        "json-serializer": {
            "base-classes": ["MarshmallowSerializer"],
            "class": f"{module}.resources.records.ui.TestUIJSONSerializer",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "flask_resources.BaseListSchema"},
                {"import": "flask_resources.MarshmallowSerializer"},
                {"import": "flask_resources.serializers.JSONSerializer"},
            ],
            "module": f"{module}.resources.records.ui",
        },
        "mapping": {
            "alias": "my_test_record",
            "file": "my/test/records/mappings/os-v2/my_test_record/test-1.0.0.json",
            "generate": True,
            "index": "my_test_record-test-1.0.0",
            "module": f"{module}.records.mappings",
        },
        "marshmallow": {
            "base-classes": ["ma.Schema"],  # NOSONAR
            "class": f"{module}.services.records.schema.TestSchema",
            "extra-code": "",
            "generate": True,
            "module": f"{module}.services.records.schema",
        },
        "model-name": "My Test Record",
        "module": {
            "alias": "my_test_record",
            "base": "test",
            "base-upper": "TEST",
            "base-title": "Test",
            "kebab-module": "my-test",
            "path": "my/test",
            "prefix": "Test",
            "prefix-snake": "test",
            "prefix-upper": "TEST",
            "qualified": f"{module}",
            "suffix": "test",
            "suffix-snake": "test",
            "suffix-upper": "TEST",
        },
        "permissions": {
            "base-classes": ["RecordPermissionPolicy"],
            "class": f"{module}.services.records.permissions.TestPermissionPolicy",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_permissions.RecordPermissionPolicy"}
            ],
            "module": f"{module}.services.records.permissions",
            "presets": ["everyone"],
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
            "module": f"{module}.records.api",
            "provider-base-classes": ["RecordIdProviderV2"],
            "provider-class": f"{module}.records.api.TestIdProvider",
            "type": "mytcrd",
        },
        "properties": {
            "metadata": {
                "marshmallow": {
                    "base-classes": ["ma.Schema"],
                    "class": f"{module}.services.records.schema.TestMetadataSchema",
                    "extra-code": "",
                    "generate": True,
                    "module": f"{module}.services.records.schema",
                },
                "properties": {},
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "base-classes": ["ma.Schema"],
                        "class": f"{module}.services.records.ui_schema.TestMetadataUISchema",
                        "extra-code": "",
                        "generate": True,
                        "module": f"{module}.services.records.ui_schema",
                    }
                },
            }
        },
        "proxy": {"module": f"{module}.proxies", "generate": True},
        "record": {
            "base-classes": ["InvenioRecord"],
            "class": f"{module}.records.api.TestRecord",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioRecord",
                    "import": "invenio_records_resources.records.api.Record",
                }
            ],
            "module": f"{module}.records.api",
        },
        "record-dumper": {
            "base-classes": ["SearchDumper"],
            "class": f"{module}.records.dumper.TestDumper",
            "extensions": [],
            "extra-code": "",
            "generate": True,
            "imports": [{"import": "invenio_records.dumpers.SearchDumper"}],
            "module": f"{module}.records.dumper",
        },
        "record-metadata": {
            "alembic": f"{module}.alembic",
            "alias": "my_test_record",
            "base-classes": ["db.Model", "RecordMetadataBase"],
            "class": f"{module}.records.models.TestMetadata",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records.models.RecordMetadataBase"},
                {"import": "invenio_db.db"},
            ],
            "module": f"{module}.records.models",
            "table": "test_metadata",
            "use-versioning": True,
        },
        "resource": {
            "base-classes": ["RecordResource"],
            "class": f"{module}.resources.records.resource.TestResource",
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResource"}
            ],
            "module": f"{module}.resources.records.resource",
            "proxy": "current_resource",
        },
        "resource-config": {
            "base-classes": ["RecordResourceConfig"],
            "base-url": "/my-test/",
            "base-html-url": "/my-test/",
            "class": f"{module}.resources.records.config.TestResourceConfig",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResourceConfig"}
            ],
            "module": f"{module}.resources.records.config",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "saved-model": {
            "alias": "my_test_record",
            "file": "my/test/models/records.json",
            "module": f"{module}.models",
        },
        "search-options": {
            "base-classes": ["InvenioSearchOptions"],
            "class": f"{module}.services.records.search.TestSearchOptions",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioSearchOptions",
                    "import": "invenio_records_resources.services.SearchOptions",
                }
            ],
            "module": f"{module}.services.records.search",
        },
        "searchable": True,
        "service": {
            "base-classes": ["InvenioRecordService"],
            "class": f"{module}.services.records.service.TestService",
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioRecordService",
                    "import": "invenio_records_resources.services.RecordService",
                }
            ],
            "module": f"{module}.services.records.service",
            "proxy": "current_service",
        },
        "service-config": {
            "base-classes": [
                "PermissionsPresetsConfigMixin",
                "InvenioRecordServiceConfig",
            ],
            "class": f"{module}.services.records.config.TestServiceConfig",
            "components": [],
            "config-key": "TEST_RECORD_SERVICE_CONFIG",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioRecordServiceConfig",
                    "import": "invenio_records_resources.services.RecordServiceConfig",
                },
                {
                    "import": "oarepo_runtime.config.service.PermissionsPresetsConfigMixin"
                },
            ],
            "module": f"{module}.services.records.config",
            "service-id": "test",
        },
        "sortable": [],
        "type": "model",
        "ui": {
            "marshmallow": {
                "base-classes": ["InvenioUISchema"],
                "class": f"{module}.services.records.ui_schema.TestUISchema",
                "extra-code": "",
                "generate": True,
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
                "module": f"{module}.services.records.ui_schema",
            }
        },
        "app-blueprint": {
            "alias": "my_test_record",
            "extra_code": "",
            "function": f"{module}.views.records.app.create_app_blueprint",
            "generate": True,
            "imports": [],
            "module": f"{module}.views.records.app",
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
