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
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "record-service-config-bases": [
            "invenio_records_resources.services.RecordServiceConfig"
        ],
        "record-metadata-class": "test.records.models.TestMetadata",
        "record-api-blueprints-setup-cfg": "test",
        "config-package": "test.config",
        "saved-model-file": "test/models/model.json",
        "record-service-class": "test.services.records.service.TestService",
        "invenio-proxies-extra-code": "",
        "jsonschemas-package": "test.records.jsonschemas",
        "record-jsonschemas-setup-cfg": "test",
        "type": "model",
        "service-id": "test",
        "record-schema-class": "test.services.records.schema.TestRecordSchema",
        "record-metadata-bases": ["invenio_records.models.RecordMetadataBase"],
        "generate-record-pid-field": True,
        "flask-extension-name": "test",
        "mapping-package": "test.records.mappings",
        "record-class": "test.records.api.TestRecord",
        "record-dumper-extensions": [],
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "pid-field-cls": "PIDField",
        "invenio-views-extra-code": "",
        "proxies-current-resource": "test.proxies.current_resource",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "record-schema-metadata-setup-cfg": "test",
        "ext-class": "test.ext.TestExt",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "index-name": "test-test-1.0.0",
        "config-dummy-class": "test.config.DummyClass",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "invenio-record-permissions-extra-code": "",
        "record-resource-config-bases": [
            "invenio_records_resources.resources.RecordResourceConfig"
        ],
        "package-base": "test",
        "record-facets-class": "test.services.records.facets.Test",
        "invenio-record-service-extra-code": "",
        "invenio-record-extra-code": "",
        "record-service-config-components": [
            "oarepo_runtime.relations.components.CachingRelationsComponent"
        ],
        "pid-field-imports": [
            {"import": "invenio_records_resources.records.systemfields.pid.PIDField"},
            {
                "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
            },
            {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
        ],
        "record-resource-bases": ["invenio_records_resources.resources.RecordResource"],
        "record-metadata-table-name": "test_metadata",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "collection-url": "/test/",
        "oarepo-models-setup-cfg": "test",
        "record-schema-metadata-alembic": "test",
        "invenio-ext-extra-code": "",
        "record-service-bases": ["invenio_records_resources.services.RecordService"],
        "record-records-package": "test.records",
        "record-ui-schema-class": "test.services.records.ui_schema.TestRecordUISchema",
        "invenio-version-extra-code": "",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "record-pid-provider-class": "test.records.api.TestIdProvider",
        "package-path": "test",
        "record-pid-provider-bases": [
            "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"
        ],
        "schema-version": "1.0.0",
        "permissions": {"presets": []},
        "schema-name": "test-1.0.0.json",
        "invenio-record-resource-config-extra-code": "",
        "invenio-record-schema-extra-code": "",
        "package-base-upper": "TEST",
        "extension-suffix": "test",
        "model-name": "test",
        "invenio-record-object-schema-extra-code": "",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "cli-function": "test.cli.group",
        "invenio-record-resource-extra-code": "",
        "invenio-record-service-config-extra-code": "",
        "pid-field-provider": "RecordIdProviderV2",
        "invenio-config-extra-code": "",
        "script-import-sample-data": "data/sample_data.yaml",
        "profile-package": "records",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "ui": {
            "marshmallow": {
                "generate": True,
                "schema-class": "test.services.records.ui_schema.TestRecordUISchema",
                "base-classes": ["InvenioUISchema"],
            }
        },
        "schema-server": "local://",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "record-resource-blueprint-name": "Test",
        "record-resources-package": "test.resources.records",
        "invenio-record-facets-extra-code": "",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "invenio-record-dumper-extra-code": "",
        "flask-commands-setup-cfg": "test",
        "pid-field-context": "PIDFieldContext",
        "record-prefix": "Test",
        "record-services-package": "test.services.records",
        "invenio-record-metadata-extra-code": "",
        "record-prefix-snake": "test",
        "record-bases": ["invenio_records_resources.records.api.Record"],
        "package": "test",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "pid-type": "test",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "kebap-package": "test",
        "record-service-config-generate-links": True,
        "proxies-current-service": "test.proxies.current_service",
        "invenio-record-search-options-extra-code": "",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "record-mapping-setup-cfg": "test",
        "record-blueprints-setup-cfg": "test",
        "marshmallow": {
            "generate": True,
            "schema-class": "test.services.records.schema.TestRecordSchema",
            "base-classes": ["ma.Schema"],
        },
        "pid-field-args": ["create=True"],
        "properties": {
            "a": {"type": "keyword"},
            "b": {
                "type": "object",
                "marshmallow": {
                    "generate": True,
                    "schema-class": "test.services.records.schema.BSchema",
                },
                "ui": {
                    "marshmallow": {
                        "generate": True,
                        "schema-class": "test.services.records.ui_schema.BUISchema",
                    }
                },
                "properties": {"c": {"type": "keyword"}},
            },
            "metadata": {
                "type": "object",
                "marshmallow": {
                    "generate": True,
                    "schema-class": "test.services.records.schema.TestMetadataSchema",
                    "base-classes": ["ma.Schema"],
                },
                "ui": {
                    "marshmallow": {
                        "generate": True,
                        "schema-class": "test.services.records.ui_schema.TestMetadataUISchema",
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
oarepo.models = test = test.models:model.json"""
    )


def build(model, output_builder_components=None):
    builder = ModelBuilder(
        output_builders=[
            ModelSaverBuilder,
            ModelRegistrationBuilder,
        ],
        outputs=[JSONOutput, PythonOutput, CFGOutput],
        model_preprocessors=[
            DefaultValuesModelPreprocessor,
            InvenioModelPreprocessor,
            InvenioBaseClassesModelPreprocessor,
        ],
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
                    },
                },
                "model": {
                    **model,
                    "package": "test",
                    "record-prefix": "Test",
                },
            },
            included_models=load_included_models_from_entry_points(),
            loaders=load_entry_points_dict("oarepo_model_builder.loaders"),
        ),
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
        "record-service-config-generate-links": True,
        "record-resource-config-bases": [
            "invenio_records_resources.resources.RecordResourceConfig"
        ],
        "invenio-record-metadata-extra-code": "",
        "invenio-config-extra-code": "",
        "invenio-record-dumper-extra-code": "",
        "record-services-package": "test.services.records",
        "mapping-package": "test.records.mappings",
        "service-id": "test",
        "invenio-record-extra-code": "",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "invenio-record-facets-extra-code": "",
        "record-resource-blueprint-name": "Test",
        "record-dumper-extensions": [],
        "record-metadata-class": "test.records.models.TestMetadata",
        "proxies-current-service": "test.proxies.current_service",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "saved-model-file": "test/models/model.json",
        "script-import-sample-data": "data/sample_data.yaml",
        "ext-class": "test.ext.TestExt",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "invenio-record-resource-config-extra-code": "",
        "collection-url": "/test/",
        "package-path": "test",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "kebap-package": "test",
        "pid-field-args": ["create=True"],
        "marshmallow": {
            "generate": True,
            "base-classes": ["InvenioBaseRecordSchema"],
            "schema-class": "test.services.records.schema.TestRecordSchema",
        },
        "record-prefix": "Test",
        "pid-field-imports": [
            {"import": "invenio_records_resources.records.systemfields.pid.PIDField"},
            {
                "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
            },
            {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
        ],
        "oarepo-models-setup-cfg": "test",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "invenio-version-extra-code": "",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "record-resource-bases": ["invenio_records_resources.resources.RecordResource"],
        "record-service-config-components": [
            "oarepo_runtime.relations.components.CachingRelationsComponent"
        ],
        "jsonschemas-package": "test.records.jsonschemas",
        "flask-extension-name": "test",
        "invenio-views-extra-code": "",
        "generate-record-pid-field": True,
        "record-bases": ["invenio_records_resources.records.api.Record"],
        "invenio-proxies-extra-code": "",
        "record-blueprints-setup-cfg": "test",
        "record-schema-metadata-alembic": "test",
        "schema-version": "1.0.0",
        "schema-name": "test-1.0.0.json",
        "flask-commands-setup-cfg": "test",
        "invenio-record-service-config-extra-code": "",
        "pid-field-provider": "RecordIdProviderV2",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "profile-package": "records",
        "invenio-record-schema-extra-code": "",
        "config-dummy-class": "test.config.DummyClass",
        "record-metadata-table-name": "test_metadata",
        "ui": {
            "marshmallow": {
                "generate": True,
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
                "base-classes": ["InvenioUISchema"],
                "schema-class": "test.services.records.ui_schema.TestRecordUISchema",
            }
        },
        "invenio-record-search-options-extra-code": "",
        "pid-field-cls": "PIDField",
        "package-base-upper": "TEST",
        "record-records-package": "test.records",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "package": "test",
        "record-schema-class": "test.services.records.schema.TestRecordSchema",
        "record-mapping-setup-cfg": "test",
        "record-api-blueprints-setup-cfg": "test",
        "record-ui-schema-class": "test.services.records.ui_schema.TestRecordUISchema",
        "record-pid-provider-class": "test.records.api.TestIdProvider",
        "record-service-config-bases": [
            "invenio_records_resources.services.RecordServiceConfig"
        ],
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "record-pid-provider-bases": [
            "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"
        ],
        "index-name": "test-test-1.0.0",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "invenio-record-resource-extra-code": "",
        "record-service-class": "test.services.records.service.TestService",
        "pid-field-context": "PIDFieldContext",
        "record-class": "test.records.api.TestRecord",
        "record-resources-package": "test.resources.records",
        "invenio-ext-extra-code": "",
        "invenio-record-object-schema-extra-code": "",
        "record-facets-class": "test.services.records.facets.Test",
        "record-jsonschemas-setup-cfg": "test",
        "model-name": "test",
        "permissions": {"presets": []},
        "invenio-record-permissions-extra-code": "",
        "type": "model",
        "extension-suffix": "test",
        "pid-type": "test",
        "record-metadata-bases": ["invenio_records.models.RecordMetadataBase"],
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "proxies-current-resource": "test.proxies.current_resource",
        "config-package": "test.config",
        "package-base": "test",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "record-service-bases": ["invenio_records_resources.services.RecordService"],
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "record-schema-metadata-setup-cfg": "test",
        "cli-function": "test.cli.group",
        "schema-server": "local://",
        "invenio-record-service-extra-code": "",
        "record-prefix-snake": "test",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "properties": {
            "$schema": {
                "sample": {"skip": True},
                "type": "keyword",
                "ui": {"marshmallow": {"write": False, "read": False}},
                "marshmallow": {"write": False, "read": False},
                "facets": {"searchable": True},
            },
            "created": {
                "sample": {"skip": True},
                "type": "datetime",
                "ui": {"marshmallow": {"write": False, "read": False}},
                "marshmallow": {"write": False, "read": False},
                "facets": {"searchable": True},
            },
            "id": {
                "sample": {"skip": True},
                "type": "keyword",
                "ui": {"marshmallow": {"write": False, "read": False}},
                "marshmallow": {"write": False, "read": False},
                "facets": {"searchable": True},
            },
            "updated": {
                "sample": {"skip": True},
                "type": "datetime",
                "ui": {"marshmallow": {"write": False, "read": False}},
                "marshmallow": {"write": False, "read": False},
                "facets": {"searchable": True},
            },
        },
    }
