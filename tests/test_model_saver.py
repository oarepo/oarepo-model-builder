import json
import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.model_saver import (
    ModelRegistrationBuilder,
    ModelSaverBuilder,
)
from oarepo_model_builder.entrypoints import (
    load_entry_points_dict,
    load_included_models_from_entry_points,
)
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.outputs.json import JSONOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema.schema import ModelSchema

try:
    import json5
except ImportError:
    import json as json5


def test_model_saver():
    data = build(
        {
            "properties": {
                "a": {"type": "keyword"},
                "b": {
                    "type": "object",
                    "properties": {
                        "c": {
                            "type": "keyword",
                        }
                    },
                    "marshmallow": {"generate": True},
                },
                "metadata": {"properties": {}},
            }
        },
    )
    assert data[0]["model"] == {
        "type": "model",
        "searchable": True,
        "module": {
            "qualified": "test",
            "alias": "test",
            "path": "test",
            "base": "test",
            "base-upper": "TEST",
            "base-title": "Test",
            "kebab-module": "test",
            "prefix": "Test",
            "prefix-upper": "TEST",
            "prefix-snake": "test",
            "suffix": "test",
            "suffix-upper": "TEST",
            "suffix-snake": "test",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "model-name": "Test",
        "ext-resource": {"generate": True, "skip": False},
        "search-options": {
            "generate": True,
            "module": "test.services.records.search",
            "extra-code": "",
            "class": "test.services.records.search.TestSearchOptions",
            "base-classes": [
                "invenio_records_resources.services.SearchOptions{InvenioSearchOptions}"
            ],
            "imports": [],
            "fields": {},
            "sort-options-field": "sort_options",
        },
        "config": {
            "generate": True,
            "module": "test.config",
            "extra_code": "",
            "imports": [],
        },
        "ext": {
            "generate": True,
            "module": "test.ext",
            "class": "test.ext.TestExt",
            "base-classes": [],
            "extra_code": "",
            "alias": "test",
            "imports": [],
        },
        "api-blueprint": {
            "generate": True,
            "alias": "test",
            "extra_code": "",
            "module": "test.views.records.api",
            "function": "test.views.records.api.create_api_blueprint",
            "imports": [],
        },
        "app-blueprint": {
            "generate": True,
            "alias": "test",
            "extra_code": "",
            "module": "test.views.records.app",
            "function": "test.views.records.app.create_app_blueprint",
            "imports": [],
        },
        "facets": {
            "generate": True,
            "module": "test.services.records.facets",
            "groups": True,
            "extra-code": "",
        },
        "record": {
            "generate": True,
            "module": "test.records.api",
            "class": "test.records.api.TestRecord",
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
            "module": "test.resources.records.resource",
            "class": "test.resources.records.resource.TestResource",
            "proxy": "current_resource",
            "extra-code": "",
            "base-classes": ["invenio_records_resources.resources.RecordResource"],
            "additional-args": [],
            "imports": [],
        },
        "resource-config": {
            "generate": True,
            "base-url": "/test/",
            "base-html-url": "/test/",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "module": "test.resources.records.config",
            "class": "test.resources.records.config.TestResourceConfig",
            "extra-code": "",
            "base-classes": [
                "invenio_records_resources.resources.RecordResourceConfig"
            ],
            "additional-args": [],
            "imports": [],
        },
        "saved-model": {
            "file": "test/models/records.json",
            "module": "test.models",
            "alias": "test",
        },
        "proxy": {"module": "test.proxies", "generate": True},
        "json-schema-settings": {
            "generate": True,
            "alias": "test",
            "version": "1.0.0",
            "module": "test.records.jsonschemas",
            "name": "test-1.0.0.json",
            "file": "test/records/jsonschemas/test-1.0.0.json",
        },
        "pid": {
            "generate": True,
            "type": "test",
            "module": "test.records.api",
            "provider-class": "test.records.api.TestIdProvider",
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
            "module": "test.records.dumpers.dumper",
            "class": "test.records.dumpers.dumper.TestDumper",
            "base-classes": ["oarepo_runtime.records.dumpers.SearchDumper"],
            "extra-code": "",
            "extensions": ["{{test.records.dumpers.edtf.TestEDTFIntervalDumperExt}}()"],
            "imports": [],
        },
        "record-metadata": {
            "generate": True,
            "module": "test.records.models",
            "class": "test.records.models.TestMetadata",
            "base-classes": [
                "invenio_db.db{db.Model}",
                "invenio_records.models.RecordMetadataBase",
            ],
            "extra-code": "",
            "imports": [],
            "table": "test_metadata",
            "alias": "test",
            "use-versioning": True,
            "alembic": "test.alembic",
        },
        "service-config": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CONFIG",
            "module": "test.services.records.config",
            "class": "test.services.records.config.TestServiceConfig",
            "extra-code": "",
            "service-id": "test",
            "base-classes": [
                "oarepo_runtime.services.config.service.PermissionsPresetsConfigMixin",
                "invenio_records_resources.services.RecordServiceConfig{InvenioRecordServiceConfig}",
            ],
            "additional-args": [],
            "components": [],
        },
        "service": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "proxy": "current_service",
            "module": "test.services.records.service",
            "class": "test.services.records.service.TestService",
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
                "module": "test.services.records.ui_schema",
                "class": "test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
                "base-classes": ["oarepo_runtime.services.schema.ui.InvenioUISchema"],
                "imports": [],
            }
        },
        "json-serializer": {
            "module": "test.resources.records.ui",
            "class": "test.resources.records.ui.TestUIJSONSerializer",
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
            "alias": "test",
            "module": "test.records.mappings",
            "index": "test-test-1.0.0",
            "file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        },
        "marshmallow": {
            "generate": True,
            "module": "test.services.records.schema",
            "class": "test.services.records.schema.TestSchema",
            "extra-code": "",
            "base-classes": ["marshmallow.Schema"],
        },
        "permissions": {
            "generate": True,
            "presets": ["everyone"],
            "extra-code": "",
            "module": "test.services.records.permissions",
            "class": "test.services.records.permissions.TestPermissionPolicy",
            "base-classes": ["invenio_records_permissions.RecordPermissionPolicy"],
            "imports": [],
        },
        "edtf-interval-dumper": {
            "generate": True,
            "module": "test.records.dumpers.edtf",
            "class": "test.records.dumpers.edtf.TestEDTFIntervalDumperExt",
            "base-classes": [
                "oarepo_runtime.records.dumpers.edtf_interval.EDTFIntervalDumperExt"
            ],
            "extra-code": "",
            "extensions": [],
            "imports": [],
        },
        "record-list": {
            "generate": True,
            "module": "test.services.records.results",
            "class": "test.services.records.results.TestRecordList",
            "extra-code": "",
            "base-classes": ["oarepo_runtime.services.results.RecordList"],
            "components": [],
            "imports": [],
        },
        "record-item": {
            "generate": True,
            "module": "test.services.records.results",
            "class": "test.services.records.results.TestRecordItem",
            "extra-code": "",
            "base-classes": ["oarepo_runtime.services.results.RecordItem"],
            "components": [],
            "imports": [],
        },
        "sortable": [],
        "properties": {
            "a": {"type": "keyword"},
            "b": {
                "type": "object",
                "marshmallow": {
                    "generate": True,
                    "class": "test.services.records.schema.BSchema",
                },
                "ui": {
                    "marshmallow": {
                        "generate": True,
                        "class": "test.services.records.ui_schema.BUISchema",
                    }
                },
                "properties": {"c": {"type": "keyword"}},
            },
            "metadata": {
                "type": "object",
                "marshmallow": {
                    "module": "test.services.records.schema",
                    "generate": True,
                    "class": "test.services.records.schema.TestMetadataSchema",
                    "extra-code": "",
                    "base-classes": ["marshmallow.Schema"],
                },
                "ui": {
                    "marshmallow": {
                        "generate": True,
                        "module": "test.services.records.ui_schema",
                        "class": "test.services.records.ui_schema.TestMetadataUISchema",
                        "extra-code": "",
                        "base-classes": ["marshmallow.Schema"],
                    }
                },
            },
        },
    }

    assert data[1].strip() == ""
    assert (
        data[2].strip()
        == """[options.entry_points]
oarepo.models = test = test.models:records.json"""
    )


def build(model, output_builder_components=None):
    builder = ModelBuilder(
        output_builders=[
            ModelSaverBuilder,
            ModelRegistrationBuilder,
        ],
        outputs=[JSONOutput, PythonOutput, CFGOutput],
        filesystem=InMemoryFileSystem(),
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {
                        "use-isort": False,
                        "use-black": False,
                        "use-autoflake": False,
                    },
                },
                "record": {**model, "module": {"qualified": "test"}},
            },
            included_models=load_included_models_from_entry_points(),
            loaders=load_entry_points_dict("oarepo_model_builder.loaders"),
        ),
        profile="record",
        model_path=["record"],
        output_dir="",
    )
    return (
        json5.load(
            builder.filesystem.open(os.path.join("test", "models", "records.json"))
        ),
        builder.filesystem.read(os.path.join("test", "models", "__init__.py")),
        builder.filesystem.read("setup.cfg"),
    )


def test_model_saver_invenio():
    data = build(
        {"use": "invenio", "properties": {}},
    )
    print(repr(data[0]))
    assert data[0]["model"] == {
        "type": "model",
        "marshmallow": {
            "imports": [],
            "base-classes": [
                "oarepo_runtime.services.schema.marshmallow.BaseRecordSchema"
            ],
            "generate": True,
            "module": "test.services.records.schema",
            "class": "test.services.records.schema.TestSchema",
            "extra-code": "",
        },
        "searchable": True,
        "ui": {
            "marshmallow": {
                "imports": [],
                "base-classes": ["oarepo_runtime.services.schema.ui.InvenioUISchema"],
                "generate": True,
                "module": "test.services.records.ui_schema",
                "class": "test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
            }
        },
        "module": {
            "qualified": "test",
            "alias": "test",
            "path": "test",
            "base": "test",
            "base-upper": "TEST",
            "base-title": "Test",
            "kebab-module": "test",
            "prefix": "Test",
            "prefix-upper": "TEST",
            "prefix-snake": "test",
            "suffix": "test",
            "suffix-upper": "TEST",
            "suffix-snake": "test",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "model-name": "Test",
        "ext-resource": {"generate": True, "skip": False},
        "search-options": {
            "generate": True,
            "module": "test.services.records.search",
            "extra-code": "",
            "class": "test.services.records.search.TestSearchOptions",
            "base-classes": [
                "invenio_records_resources.services.SearchOptions{InvenioSearchOptions}"
            ],
            "imports": [],
            "fields": {},
            "sort-options-field": "sort_options",
        },
        "config": {
            "generate": True,
            "module": "test.config",
            "extra_code": "",
            "imports": [],
        },
        "ext": {
            "generate": True,
            "module": "test.ext",
            "class": "test.ext.TestExt",
            "base-classes": [],
            "extra_code": "",
            "alias": "test",
            "imports": [],
        },
        "api-blueprint": {
            "generate": True,
            "alias": "test",
            "extra_code": "",
            "module": "test.views.records.api",
            "function": "test.views.records.api.create_api_blueprint",
            "imports": [],
        },
        "app-blueprint": {
            "generate": True,
            "alias": "test",
            "extra_code": "",
            "module": "test.views.records.app",
            "function": "test.views.records.app.create_app_blueprint",
            "imports": [],
        },
        "facets": {
            "generate": True,
            "module": "test.services.records.facets",
            "groups": True,
            "extra-code": "",
        },
        "record": {
            "generate": True,
            "module": "test.records.api",
            "class": "test.records.api.TestRecord",
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
            "module": "test.resources.records.resource",
            "class": "test.resources.records.resource.TestResource",
            "proxy": "current_resource",
            "extra-code": "",
            "base-classes": ["invenio_records_resources.resources.RecordResource"],
            "additional-args": [],
            "imports": [],
        },
        "resource-config": {
            "generate": True,
            "base-url": "/test/",
            "base-html-url": "/test/",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "module": "test.resources.records.config",
            "class": "test.resources.records.config.TestResourceConfig",
            "extra-code": "",
            "base-classes": [
                "invenio_records_resources.resources.RecordResourceConfig"
            ],
            "additional-args": [],
            "imports": [],
        },
        "saved-model": {
            "file": "test/models/records.json",
            "module": "test.models",
            "alias": "test",
        },
        "proxy": {"module": "test.proxies", "generate": True},
        "json-schema-settings": {
            "generate": True,
            "alias": "test",
            "version": "1.0.0",
            "module": "test.records.jsonschemas",
            "name": "test-1.0.0.json",
            "file": "test/records/jsonschemas/test-1.0.0.json",
        },
        "pid": {
            "generate": True,
            "type": "test",
            "module": "test.records.api",
            "provider-class": "test.records.api.TestIdProvider",
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
            "module": "test.records.dumpers.dumper",
            "class": "test.records.dumpers.dumper.TestDumper",
            "base-classes": ["oarepo_runtime.records.dumpers.SearchDumper"],
            "extra-code": "",
            "extensions": ["{{test.records.dumpers.edtf.TestEDTFIntervalDumperExt}}()"],
            "imports": [],
        },
        "record-metadata": {
            "generate": True,
            "module": "test.records.models",
            "class": "test.records.models.TestMetadata",
            "base-classes": [
                "invenio_db.db{db.Model}",
                "invenio_records.models.RecordMetadataBase",
            ],
            "extra-code": "",
            "imports": [],
            "table": "test_metadata",
            "alias": "test",
            "use-versioning": True,
            "alembic": "test.alembic",
        },
        "service-config": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CONFIG",
            "module": "test.services.records.config",
            "class": "test.services.records.config.TestServiceConfig",
            "extra-code": "",
            "service-id": "test",
            "base-classes": [
                "oarepo_runtime.services.config.service.PermissionsPresetsConfigMixin",
                "invenio_records_resources.services.RecordServiceConfig{InvenioRecordServiceConfig}",
            ],
            "additional-args": [],
            "components": [],
        },
        "service": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "proxy": "current_service",
            "module": "test.services.records.service",
            "class": "test.services.records.service.TestService",
            "extra-code": "",
            "base-classes": [
                "invenio_records_resources.services.RecordService{InvenioRecordService}"
            ],
            "additional-args": [],
            "imports": [],
        },
        "json-serializer": {
            "module": "test.resources.records.ui",
            "class": "test.resources.records.ui.TestUIJSONSerializer",
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
            "alias": "test",
            "module": "test.records.mappings",
            "index": "test-test-1.0.0",
            "file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        },
        "permissions": {
            "generate": True,
            "presets": ["everyone"],
            "extra-code": "",
            "module": "test.services.records.permissions",
            "class": "test.services.records.permissions.TestPermissionPolicy",
            "base-classes": ["invenio_records_permissions.RecordPermissionPolicy"],
            "imports": [],
        },
        "edtf-interval-dumper": {
            "generate": True,
            "module": "test.records.dumpers.edtf",
            "class": "test.records.dumpers.edtf.TestEDTFIntervalDumperExt",
            "base-classes": [
                "oarepo_runtime.records.dumpers.edtf_interval.EDTFIntervalDumperExt"
            ],
            "extra-code": "",
            "extensions": [],
            "imports": [],
        },
        "record-list": {
            "generate": True,
            "module": "test.services.records.results",
            "class": "test.services.records.results.TestRecordList",
            "extra-code": "",
            "base-classes": ["oarepo_runtime.services.results.RecordList"],
            "components": [],
            "imports": [],
        },
        "record-item": {
            "generate": True,
            "module": "test.services.records.results",
            "class": "test.services.records.results.TestRecordItem",
            "extra-code": "",
            "base-classes": ["oarepo_runtime.services.results.RecordItem"],
            "components": [],
            "imports": [],
        },
        "sortable": [],
        "properties": {
            "$schema": {
                "type": "keyword",
                "marshmallow": {"read": False, "write": False},
                "facets": {"searchable": True, "facet": False},
                "ui": {"marshmallow": {"read": False, "write": False}},
                "sample": {"skip": True},
            },
            "created": {
                "type": "datetime",
                "facets": {"searchable": True, "facet": False},
                "ui": {"marshmallow": {"read": False, "write": False}},
                "marshmallow": {"read": False, "write": False},
                "sample": {"skip": True},
            },
            "id": {
                "type": "keyword",
                "marshmallow": {"read": False, "write": False},
                "facets": {"searchable": True, "facet": False},
                "ui": {"marshmallow": {"read": False, "write": False}},
                "sample": {"skip": True},
            },
            "updated": {
                "type": "datetime",
                "facets": {"searchable": True, "facet": False},
                "ui": {"marshmallow": {"read": False, "write": False}},
                "marshmallow": {"read": False, "write": False},
                "sample": {"skip": True},
            },
        },
    }
