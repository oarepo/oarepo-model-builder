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
from oarepo_model_builder.schema import ModelSchema

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
        "sortable": [],
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
            "base-classes": ["InvenioSearchOptions"],
            "imports": [
                {
                    "import": "invenio_records_resources.services.SearchOptions",
                    "alias": "InvenioSearchOptions",
                }
            ],
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
            "extra-code": "",
        },
        "record": {
            "generate": True,
            "module": "test.records.api",
            "class": "test.records.api.TestRecord",
            "base-classes": ["InvenioRecord"],
            "imports": [
                {
                    "import": "invenio_records_resources.records.api.Record",
                    "alias": "InvenioRecord",
                }
            ],
            "extra-code": "",
        },
        "resource": {
            "generate": True,
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "module": "test.resources.records.resource",
            "class": "test.resources.records.resource.TestResource",
            "proxy": "current_resource",
            "extra-code": "",
            "base-classes": ["RecordResource"],
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResource"}
            ],
        },
        "resource-config": {
            "generate": True,
            "base-url": "/test/",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "module": "test.resources.records.config",
            "class": "test.resources.records.config.TestResourceConfig",
            "extra-code": "",
            "base-classes": ["RecordResourceConfig"],
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResourceConfig"}
            ],
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
            "provider-base-classes": ["RecordIdProviderV2"],
            "field-class": "PIDField",
            "context-class": "PIDFieldContext",
            "field-args": ["create=True"],
            "imports": [
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDField"
                },
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
                },
                {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
            ],
        },
        "record-dumper": {
            "generate": True,
            "module": "test.records.dumper",
            "class": "test.records.dumper.TestDumper",
            "base-classes": ["SearchDumper"],
            "extra-code": "",
            "extensions": [],
            "imports": [{"import": "invenio_records.dumpers.SearchDumper"}],
        },
        "record-metadata": {
            "generate": True,
            "module": "test.records.models",
            "class": "test.records.models.TestMetadata",
            "base-classes": ["db.Model", "RecordMetadataBase"],
            "extra-code": "",
            "imports": [
                {"import": "invenio_records.models.RecordMetadataBase"},
                {"import": "invenio_db.db"},
            ],
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
                "PermissionsPresetsConfigMixin",
                "InvenioRecordServiceConfig",
            ],
            "components": [],
            "imports": [
                {
                    "import": "invenio_records_resources.services.RecordServiceConfig",
                    "alias": "InvenioRecordServiceConfig",
                },
                {
                    "import": "oarepo_runtime.config.service.PermissionsPresetsConfigMixin"
                },
            ],
        },
        "service": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "proxy": "current_service",
            "module": "test.services.records.service",
            "class": "test.services.records.service.TestService",
            "extra-code": "",
            "base-classes": ["InvenioRecordService"],
            "imports": [
                {
                    "import": "invenio_records_resources.services.RecordService",
                    "alias": "InvenioRecordService",
                }
            ],
        },
        "ui": {
            "marshmallow": {
                "generate": True,
                "module": "test.services.records.ui_schema",
                "class": "test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
                "base-classes": ["InvenioUISchema"],
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
            }
        },
        "json-serializer": {
            "module": "test.resources.records.ui",
            "class": "test.resources.records.ui.TestUIJSONSerializer",
            "base-classes": ["MarshmallowSerializer"],
            "imports": [
                {"import": "flask_resources.BaseListSchema"},
                {"import": "flask_resources.MarshmallowSerializer"},
                {"import": "flask_resources.serializers.JSONSerializer"},
            ],
            "extra-code": "",
            "generate": True,
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
            "base-classes": ["ma.Schema"],
        },
        "permissions": {
            "generate": True,
            "presets": ["everyone"],
            "extra-code": "",
            "module": "test.services.records.permissions",
            "class": "test.services.records.permissions.TestPermissionPolicy",
            "base-classes": ["RecordPermissionPolicy"],
            "imports": [
                {"import": "invenio_records_permissions.RecordPermissionPolicy"}
            ],
        },
        "properties": {
            "a": {"type": "keyword"},
            "b": {
                "marshmallow": {
                    "generate": True,
                    "class": "test.services.records.schema.BSchema",
                },
                "type": "object",
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
                    "base-classes": ["ma.Schema"],
                },
                "ui": {
                    "marshmallow": {
                        "generate": True,
                        "module": "test.services.records.ui_schema",
                        "class": "test.services.records.ui_schema.TestMetadataUISchema",
                        "extra-code": "",
                        "base-classes": ["ma.Schema"],
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
        "marshmallow": {
            "imports": [{"import": "oarepo_runtime.marshmallow.BaseRecordSchema"}],
            "base-classes": ["BaseRecordSchema"],
            "generate": True,
            "module": "test.services.records.schema",
            "class": "test.services.records.schema.TestSchema",
            "extra-code": "",
        },
        "ui": {
            "marshmallow": {
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
                "base-classes": ["InvenioUISchema"],
                "generate": True,
                "module": "test.services.records.ui_schema",
                "class": "test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
            }
        },
        "searchable": True,
        "sortable": [],
        "type": "model",
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
            "base-classes": ["InvenioSearchOptions"],
            "imports": [
                {
                    "import": "invenio_records_resources.services.SearchOptions",
                    "alias": "InvenioSearchOptions",
                }
            ],
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
            "extra-code": "",
        },
        "record": {
            "generate": True,
            "module": "test.records.api",
            "class": "test.records.api.TestRecord",
            "base-classes": ["InvenioRecord"],
            "imports": [
                {
                    "import": "invenio_records_resources.records.api.Record",
                    "alias": "InvenioRecord",
                }
            ],
            "extra-code": "",
        },
        "resource": {
            "generate": True,
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "module": "test.resources.records.resource",
            "class": "test.resources.records.resource.TestResource",
            "proxy": "current_resource",
            "extra-code": "",
            "base-classes": ["RecordResource"],
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResource"}
            ],
        },
        "resource-config": {
            "generate": True,
            "base-url": "/test/",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "module": "test.resources.records.config",
            "class": "test.resources.records.config.TestResourceConfig",
            "extra-code": "",
            "base-classes": ["RecordResourceConfig"],
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResourceConfig"}
            ],
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
            "provider-base-classes": ["RecordIdProviderV2"],
            "field-class": "PIDField",
            "context-class": "PIDFieldContext",
            "field-args": ["create=True"],
            "imports": [
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDField"
                },
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
                },
                {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
            ],
        },
        "record-dumper": {
            "generate": True,
            "module": "test.records.dumper",
            "class": "test.records.dumper.TestDumper",
            "base-classes": ["SearchDumper"],
            "extra-code": "",
            "extensions": [],
            "imports": [{"import": "invenio_records.dumpers.SearchDumper"}],
        },
        "record-metadata": {
            "generate": True,
            "module": "test.records.models",
            "class": "test.records.models.TestMetadata",
            "base-classes": ["db.Model", "RecordMetadataBase"],
            "extra-code": "",
            "imports": [
                {"import": "invenio_records.models.RecordMetadataBase"},
                {"import": "invenio_db.db"},
            ],
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
                "PermissionsPresetsConfigMixin",
                "InvenioRecordServiceConfig",
            ],
            "components": [],
            "imports": [
                {
                    "import": "invenio_records_resources.services.RecordServiceConfig",
                    "alias": "InvenioRecordServiceConfig",
                },
                {
                    "import": "oarepo_runtime.config.service.PermissionsPresetsConfigMixin"
                },
            ],
        },
        "service": {
            "generate": True,
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "proxy": "current_service",
            "module": "test.services.records.service",
            "class": "test.services.records.service.TestService",
            "extra-code": "",
            "base-classes": ["InvenioRecordService"],
            "imports": [
                {
                    "import": "invenio_records_resources.services.RecordService",
                    "alias": "InvenioRecordService",
                }
            ],
        },
        "json-serializer": {
            "module": "test.resources.records.ui",
            "class": "test.resources.records.ui.TestUIJSONSerializer",
            "base-classes": ["MarshmallowSerializer"],
            "imports": [
                {"import": "flask_resources.BaseListSchema"},
                {"import": "flask_resources.MarshmallowSerializer"},
                {"import": "flask_resources.serializers.JSONSerializer"},
            ],
            "extra-code": "",
            "generate": True,
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
            "base-classes": ["RecordPermissionPolicy"],
            "imports": [
                {"import": "invenio_records_permissions.RecordPermissionPolicy"}
            ],
        },
        "properties": {
            "$schema": {
                "facets": {"searchable": True},
                "type": "keyword",
                "sample": {"skip": True},
                "marshmallow": {"write": False, "read": False},
                "ui": {"marshmallow": {"write": False, "read": False}},
            },
            "created": {
                "facets": {"searchable": True},
                "type": "datetime",
                "sample": {"skip": True},
                "marshmallow": {"write": False, "read": False},
                "ui": {"marshmallow": {"write": False, "read": False}},
            },
            "id": {
                "facets": {"searchable": True},
                "type": "keyword",
                "sample": {"skip": True},
                "marshmallow": {"write": False, "read": False},
                "ui": {"marshmallow": {"write": False, "read": False}},
            },
            "updated": {
                "facets": {"searchable": True},
                "type": "datetime",
                "sample": {"skip": True},
                "marshmallow": {"write": False, "read": False},
                "ui": {"marshmallow": {"write": False, "read": False}},
            },
        },
    }
