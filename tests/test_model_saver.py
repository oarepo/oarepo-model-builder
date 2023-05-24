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
        "api-blueprint": {
            "alias": "test",
            "extra_code": "",
            "function": "test.views.records.api.create_api_blueprint",
            "generate": True,
            "imports": [],
            "module": "test.views.records.api",
        },
        "config": {
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "test.config",
        },
        "ext": {
            "alias": "test",
            "base-classes": [],
            "class": "test.ext.TestExt",
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "test.ext",
        },
        "facets": {
            "extra-code": "",
            "generate": True,
            "module": "test.services.records.facets",
        },
        "json-schema-settings": {
            "alias": "test",
            "file": "test/records/jsonschemas/test-1.0.0.json",
            "generate": True,
            "module": "test.records.jsonschemas",
            "name": "test-1.0.0.json",
            "version": "1.0.0",
        },
        "json-serializer": {
            "base-classes": ["MarshmallowSerializer"],
            "class": "test.resources.records.ui.TestUIJSONSerializer",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "flask_resources.BaseListSchema"},
                {"import": "flask_resources.MarshmallowSerializer"},
                {"import": "flask_resources.serializers.JSONSerializer"},
            ],
            "module": "test.resources.records.ui",
        },
        "mapping-settings": {
            "alias": "test",
            "file": "test/records/mappings/os-v2/test/test-1.0.0.json",
            "generate": True,
            "index": "test-test-1.0.0",
            "module": "test.records.mappings",
        },
        "marshmallow": {
            "base-classes": ["ma.Schema"],  # NOSONAR
            "class": "test.services.records.schema.TestSchema",
            "extra-code": "",
            "generate": True,
            "module": "test.services.records.schema",  # NOSONAR
        },
        "model-name": "Test",
        "module": {
            "alias": "test",
            "base": "test",
            "base-upper": "TEST",
            "kebab-module": "test",
            "path": "test",
            "prefix": "Test",
            "prefix-snake": "test",
            "prefix-upper": "TEST",
            "qualified": "test",
            "suffix": "test",
            "suffix-snake": "test",
            "suffix-upper": "TEST",
        },
        "permissions": {
            "base-classes": ["RecordPermissionPolicy"],
            "class": "test.services.records.permissions.TestPermissionPolicy",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_permissions.RecordPermissionPolicy"}
            ],
            "module": "test.services.records.permissions",
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
            "module": "test.records.api",  # NOSONAR
            "provider-base-classes": ["RecordIdProviderV2"],
            "provider-class": "test.records.api.TestIdProvider",
            "type": "test",
        },
        "properties": {
            "a": {"type": "keyword"},
            "b": {
                "marshmallow": {
                    "class": "test.services.records.schema.BSchema",
                    "generate": True,
                },
                "properties": {"c": {"type": "keyword"}},
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "class": "test.services.records.ui_schema.BUISchema",
                        "generate": True,
                    }
                },
            },
            "metadata": {
                "marshmallow": {
                    "base-classes": ["ma.Schema"],
                    "class": "test.services.records.schema.TestMetadataSchema",
                    "extra-code": "",
                    "generate": True,
                    "module": "test.services.records.schema",
                },
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "base-classes": ["ma.Schema"],
                        "class": "test.services.records.ui_schema.TestMetadataUISchema",
                        "extra-code": "",
                        "generate": True,
                        "module": "test.services.records.ui_schema",  # NOSONAR
                    }
                },
            },
        },
        "proxy": {"module": "test.proxies", "generate": True},
        "record": {
            "base-classes": ["InvenioRecord"],
            "class": "test.records.api.TestRecord",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioRecord",
                    "import": "invenio_records_resources.records.api.Record",
                }
            ],
            "module": "test.records.api",
        },
        "record-dumper": {
            "base-classes": ["SearchDumper"],
            "class": "test.records.dumper.TestDumper",
            "extensions": [],
            "extra-code": "",
            "generate": True,
            "imports": [{"import": "invenio_records.dumpers.SearchDumper"}],
            "module": "test.records.dumper",
        },
        "record-metadata": {
            "alembic": "test.records.alembic",
            "alias": "test",
            "base-classes": ["db.Model", "RecordMetadataBase"],
            "class": "test.records.models.TestMetadata",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records.models.RecordMetadataBase"},
                {"import": "invenio_db.db"},
            ],
            "module": "test.records.models",
            "table": "test_metadata",
        },
        "resource": {
            "base-classes": ["RecordResource"],
            "class": "test.resources.records.resource.TestResource",
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResource"}
            ],
            "module": "test.resources.records.resource",
            "proxy": "current_resource",
        },
        "resource-config": {
            "base-classes": ["RecordResourceConfig"],
            "base-url": "/test/",
            "class": "test.resources.records.config.TestResourceConfig",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResourceConfig"}
            ],
            "module": "test.resources.records.config",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "saved-model": {
            "alias": "test",
            "file": "test/models/model.json",
            "module": "test.models",
        },
        "search-options": {
            "base-classes": ["InvenioSearchOptions"],
            "class": "test.services.records.search.TestSearchOptions",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioSearchOptions",
                    "import": "invenio_records_resources.services.SearchOptions",
                }
            ],
            "module": "test.services.records.search",
        },
        "searchable": True,
        "service": {
            "base-classes": ["InvenioRecordService"],
            "class": "test.services.records.service.TestService",
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioRecordService",
                    "import": "invenio_records_resources.services.RecordService",
                }
            ],
            "module": "test.services.records.service",
            "proxy": "current_service",
        },
        "service-config": {
            "base-classes": [
                "PermissionsPresetsConfigMixin",
                "InvenioRecordServiceConfig",
            ],
            "class": "test.services.records.config.TestServiceConfig",
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
            "module": "test.services.records.config",
            "service-id": "test",
        },
        "type": "model",
        "ui": {
            "marshmallow": {
                "base-classes": ["InvenioUISchema"],
                "class": "test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
                "generate": True,
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
                "module": "test.services.records.ui_schema",
            }
        },
        "app-blueprint": {
            "alias": "test",
            "extra_code": "",
            "function": "test.views.records.app.create_app_blueprint",
            "generate": True,
            "imports": [],
            "module": "test.views.records.app",
        },
    }

    assert data[1].strip() == ""
    assert (
        data[2].strip()
        == """[options.entry_points]
oarepo.models = test = test.models:model.json"""
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
            builder.filesystem.open(os.path.join("test", "models", "model.json"))
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
        "api-blueprint": {
            "alias": "test",
            "extra_code": "",
            "function": "test.views.records.api.create_api_blueprint",
            "generate": True,
            "imports": [],
            "module": "test.views.records.api",
        },
        "config": {
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "test.config",
        },
        "ext": {
            "alias": "test",
            "base-classes": [],
            "class": "test.ext.TestExt",
            "extra_code": "",
            "generate": True,
            "imports": [],
            "module": "test.ext",
        },
        "facets": {
            "extra-code": "",
            "generate": True,
            "module": "test.services.records.facets",
        },
        "json-schema-settings": {
            "alias": "test",
            "file": "test/records/jsonschemas/test-1.0.0.json",
            "generate": True,
            "module": "test.records.jsonschemas",
            "name": "test-1.0.0.json",
            "version": "1.0.0",
        },
        "json-serializer": {
            "base-classes": ["MarshmallowSerializer"],
            "class": "test.resources.records.ui.TestUIJSONSerializer",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "flask_resources.BaseListSchema"},
                {"import": "flask_resources.MarshmallowSerializer"},
                {"import": "flask_resources.serializers.JSONSerializer"},
            ],
            "module": "test.resources.records.ui",
        },
        "mapping-settings": {
            "alias": "test",
            "file": "test/records/mappings/os-v2/test/test-1.0.0.json",
            "generate": True,
            "index": "test-test-1.0.0",
            "module": "test.records.mappings",
        },
        "marshmallow": {
            "base-classes": ["InvenioBaseRecordSchema"],
            "class": "test.services.records.schema.TestSchema",
            "extra-code": "",
            "generate": True,
            "module": "test.services.records.schema",
        },
        "model-name": "Test",
        "module": {
            "alias": "test",
            "base": "test",
            "base-upper": "TEST",
            "kebab-module": "test",
            "path": "test",
            "prefix": "Test",
            "prefix-snake": "test",
            "prefix-upper": "TEST",
            "qualified": "test",
            "suffix": "test",
            "suffix-snake": "test",
            "suffix-upper": "TEST",
        },
        "permissions": {
            "base-classes": ["RecordPermissionPolicy"],
            "class": "test.services.records.permissions.TestPermissionPolicy",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_permissions.RecordPermissionPolicy"}
            ],
            "module": "test.services.records.permissions",
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
            "module": "test.records.api",
            "provider-base-classes": ["RecordIdProviderV2"],
            "provider-class": "test.records.api.TestIdProvider",
            "type": "test",
        },
        "properties": {
            "$schema": {
                "facets": {"searchable": True},
                "marshmallow": {"read": False, "write": False},
                "sample": {"skip": True},
                "type": "keyword",
                "ui": {"marshmallow": {"read": False, "write": False}},
            },
            "created": {
                "facets": {"searchable": True},
                "marshmallow": {"read": False, "write": False},
                "sample": {"skip": True},
                "type": "datetime",
                "ui": {"marshmallow": {"read": False, "write": False}},
            },
            "id": {
                "facets": {"searchable": True},
                "marshmallow": {"read": False, "write": False},
                "sample": {"skip": True},
                "type": "keyword",
                "ui": {"marshmallow": {"read": False, "write": False}},
            },
            "updated": {
                "facets": {"searchable": True},
                "marshmallow": {"read": False, "write": False},
                "sample": {"skip": True},
                "type": "datetime",
                "ui": {"marshmallow": {"read": False, "write": False}},
            },
        },
        "proxy": {"module": "test.proxies", "generate": True},
        "record": {
            "base-classes": ["InvenioRecord"],
            "class": "test.records.api.TestRecord",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioRecord",
                    "import": "invenio_records_resources.records.api.Record",
                }
            ],
            "module": "test.records.api",
        },
        "record-dumper": {
            "base-classes": ["SearchDumper"],
            "class": "test.records.dumper.TestDumper",
            "extensions": [],
            "extra-code": "",
            "generate": True,
            "imports": [{"import": "invenio_records.dumpers.SearchDumper"}],
            "module": "test.records.dumper",
        },
        "record-metadata": {
            "alembic": "test.records.alembic",
            "alias": "test",
            "base-classes": ["db.Model", "RecordMetadataBase"],
            "class": "test.records.models.TestMetadata",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records.models.RecordMetadataBase"},
                {"import": "invenio_db.db"},
            ],
            "module": "test.records.models",
            "table": "test_metadata",
        },
        "resource": {
            "base-classes": ["RecordResource"],
            "class": "test.resources.records.resource.TestResource",
            "config-key": "TEST_RECORD_RESOURCE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResource"}
            ],
            "module": "test.resources.records.resource",
            "proxy": "current_resource",
        },
        "resource-config": {
            "base-classes": ["RecordResourceConfig"],
            "base-url": "/test/",
            "class": "test.resources.records.config.TestResourceConfig",
            "config-key": "TEST_RECORD_RESOURCE_CONFIG",
            "extra-code": "",
            "generate": True,
            "imports": [
                {"import": "invenio_records_resources.resources.RecordResourceConfig"}
            ],
            "module": "test.resources.records.config",
        },
        "sample": {"file": "data/sample_data.yaml"},
        "saved-model": {
            "alias": "test",
            "file": "test/models/model.json",
            "module": "test.models",
        },
        "search-options": {
            "base-classes": ["InvenioSearchOptions"],
            "class": "test.services.records.search.TestSearchOptions",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioSearchOptions",
                    "import": "invenio_records_resources.services.SearchOptions",
                }
            ],
            "module": "test.services.records.search",
        },
        "searchable": True,
        "service": {
            "base-classes": ["InvenioRecordService"],
            "class": "test.services.records.service.TestService",
            "config-key": "TEST_RECORD_SERVICE_CLASS",
            "extra-code": "",
            "generate": True,
            "imports": [
                {
                    "alias": "InvenioRecordService",
                    "import": "invenio_records_resources.services.RecordService",
                }
            ],
            "module": "test.services.records.service",
            "proxy": "current_service",
        },
        "service-config": {
            "base-classes": [
                "PermissionsPresetsConfigMixin",
                "InvenioRecordServiceConfig",
            ],
            "class": "test.services.records.config.TestServiceConfig",
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
            "module": "test.services.records.config",
            "service-id": "test",
        },
        "type": "model",
        "ui": {
            "marshmallow": {
                "base-classes": ["InvenioUISchema"],
                "class": "test.services.records.ui_schema.TestUISchema",
                "extra-code": "",
                "generate": True,
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
                "module": "test.services.records.ui_schema",
            }
        },
        "app-blueprint": {
            "alias": "test",
            "extra_code": "",
            "function": "test.views.records.app.create_app_blueprint",
            "generate": True,
            "imports": [],
            "module": "test.views.records.app",
        },
    }
