import json
import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.model_saver import (
    ModelRegistrationBuilder,
    ModelSaverBuilder,
)
from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.entrypoints import (
    load_entry_points_dict,
    load_included_models_from_entry_points,
)
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.model_preprocessors.datatype_default import (
    DatatypeDefaultModelPreprocessor,
)
from oarepo_model_builder.model_preprocessors.default_values import (
    DefaultValuesModelPreprocessor,
)
from oarepo_model_builder.model_preprocessors.invenio import InvenioModelPreprocessor
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.outputs.json import JSONOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.datatype_preprocessor import (
    DataTypePreprocessor,
)
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.validation.model_validation import model_validator
from tests.multilang import MultilingualDataType, UIValidator

try:
    import json5
except ImportError:
    import json as json5


def test_model_saver():
    data = build(
        {
            "properties": {
                "a": {"type": "keyword", "ui": {"class": "bolder"}},
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
        property_preprocessors=[
            DataTypePreprocessor,
        ],
    )
    print(json.dumps(data[0], indent=4, sort_keys=True))
    assert data[0]["model"] == {
        "type": "object",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "pid-field-cls": "PIDField",
        "invenio-record-schema-extra-code": "",
        "schema-server": "http://localhost/schemas/",
        "invenio-record-resource-extra-code": "",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "extension-suffix": "test",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "record-schema-metadata-alembic": "test",
        "record-metadata-class": "test.records.models.TestMetadata",
        "invenio-record-metadata-extra-code": "",
        "oarepo-models-setup-cfg": "test",
        "invenio-record-extra-code": "",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "record-api-blueprints-setup-cfg": "test",
        "record-jsonschemas-setup-cfg": "test",
        "permissions": {"presets": []},
        "record-services-package": "test.services.records",
        "collection-url": "/test/",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "pid-field-provider": "RecordIdProviderV2",
        "package-path": "test",
        "schema-name": "test-1.0.0.json",
        "record-service-config-generate-links": True,
        "cli-function": "test.cli.group",
        "saved-model-file": "test/models/model.json",
        "ext-class": "test.ext.TestExt",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "jsonschemas-package": "test.records.jsonschemas",
        "marshmallow": {
            "schema-class": "test.services.records.schema.TestSchema",
            "base-classes": ["ma.Schema"],
            "generate": True,
        },
        "pid-field-context": "PIDFieldContext",
        "record-service-class": "test.services.records.service.TestService",
        "invenio-record-search-options-extra-code": "",
        "invenio-record-service-extra-code": "",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "record-schema-metadata-setup-cfg": "test",
        "package": "test",
        "record-facets-class": "test.services.records.facets.Test",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "invenio-views-extra-code": "",
        "invenio-record-service-config-extra-code": "",
        "profile-package": "records",
        "invenio-record-object-schema-extra-code": "",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "invenio-ext-extra-code": "",
        "record-resource-blueprint-name": "Test",
        "pid-field-args": ["create=True"],
        "record-schema-class": "test.services.records.schema.TestSchema",
        "generate-record-pid-field": True,
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "invenio-version-extra-code": "",
        "schema-version": "1.0.0",
        "mapping-package": "test.records.mappings",
        "record-blueprints-setup-cfg": "test",
        "invenio-record-permissions-extra-code": "",
        "properties": {
            "a": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "validators": [],
                    "imports": [],
                },
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "type": "keyword",
            },
            "b": {
                "marshmallow": {
                    "field-class": "ma_fields.Nested",
                    "schema-class": "test.services.records.schema.BSchema",
                    "validators": [],
                    "generate": True,
                    "imports": [],
                },
                "type": "object",
                "properties": {
                    "c": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [],
                            "imports": [],
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                        "type": "keyword",
                    }
                },
                "ui": {
                    "marshmallow": {
                        "field-class": "ma_fields.Nested",
                        "schema-class": "test.services.records.ui_schema.BUISchema",
                    }
                },
            },
            "metadata": {
                "marshmallow": {
                    "field-class": "ma_fields.Nested",
                    "schema-class": "test.services.records.schema.TestMetadataSchema",
                    "validators": [],
                    "base-classes": ["ma.Schema"],
                    "generate": True,
                    "imports": [],
                },
                "type": "object",
                "properties": {},
                "ui": {
                    "marshmallow": {
                        "field-class": "ma_fields.Nested",
                        "schema-class": "test.services.records.ui_schema.TestMetadataUISchema",
                        "base-classes": ["ma.Schema"],
                        "generate": True,
                    }
                },
            },
        },
        "proxies-current-resource": "test.proxies.current_resource",
        "invenio-record-dumper-extra-code": "",
        "invenio-record-facets-extra-code": "",
        "record-class": "test.records.api.TestRecord",
        "index-name": "test-test-1.0.0",
        "record-prefix-snake": "test",
        "script-import-sample-data": "data/sample_data.yaml",
        "record-metadata-table-name": "test_metadata",
        "config-package": "test.config",
        "pid-field-imports": [
            {"import": "invenio_records_resources.records.systemfields.pid.PIDField"},
            {
                "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
            },
            {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
        ],
        "package-base": "test",
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",
        "service-id": "test",
        "flask-extension-name": "test",
        "model-name": "test",
        "proxies-current-service": "test.proxies.current_service",
        "record-mapping-setup-cfg": "test",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "record-resources-package": "test.resources.records",
        "invenio-record-resource-config-extra-code": "",
        "kebap-package": "test",
        "record-dumper-extensions": [],
        "flask-commands-setup-cfg": "test",
        "package-base-upper": "TEST",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "config-dummy-class": "test.config.DummyClass",
        "record-prefix": "Test",
        "ui": {
            "marshmallow": {
                "schema-class": "test.services.records.ui_schema.TestUISchema",
                "base-classes": ["ma.Schema"],
                "generate": True,
            }
        },
        "record-records-package": "test.records",
        "invenio-proxies-extra-code": "",
        "invenio-config-extra-code": "",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
    }

    assert data[1].strip() == ""
    assert (
        data[2].strip()
        == """[options.entry_points]
oarepo.models = test = test.models:model.json"""
    )


def build(model, output_builder_components=None, property_preprocessors=None):
    datatypes._prepare_datatypes()
    if UIValidator not in model_validator.validator_map["property-ui"]:
        model_validator.validator_map["property-ui"].append(UIValidator)
    datatypes.datatype_map["multilingual"] = MultilingualDataType

    builder = ModelBuilder(
        output_builders=[
            ModelSaverBuilder,
            ModelRegistrationBuilder,
        ],
        outputs=[JSONOutput, PythonOutput, CFGOutput],
        model_preprocessors=[
            DefaultValuesModelPreprocessor,
            InvenioModelPreprocessor,
            DatatypeDefaultModelPreprocessor,
        ],
        output_builder_components=output_builder_components,
        filesystem=InMemoryFileSystem(),
        property_preprocessors=property_preprocessors,
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
        property_preprocessors=[
            DataTypePreprocessor,
        ],
    )
    print(json.dumps(data[0], indent=4))
    assert data[0]["model"] == {
        "type": "object",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "record-metadata-class": "test.records.models.TestMetadata",
        "record-records-package": "test.records",
        "record-facets-class": "test.services.records.facets.Test",
        "package": "test",
        "package-base-upper": "TEST",
        "record-prefix-snake": "test",
        "record-dumper-extensions": [],
        "invenio-record-metadata-extra-code": "",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "proxies-current-service": "test.proxies.current_service",
        "extension-suffix": "test",
        "schema-server": "http://localhost/schemas/",
        "schema-name": "test-1.0.0.json",
        "invenio-record-facets-extra-code": "",
        "properties": {
            "id": {
                "marshmallow": {
                    "read": False,
                    "write": False,
                    "field-class": "ma_fields.String",
                    "validators": [],
                    "imports": [],
                },
                "type": "keyword",
                "facets": {"searchable": True},
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "sample": {"skip": True},
            },
            "created": {
                "marshmallow": {
                    "read": False,
                    "write": False,
                    "field-class": "ma_fields.String",
                    "validators": ["validate_date('%Y-%m-%d')"],
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_date"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "type": "date",
                "facets": {"searchable": True},
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDate"}},
                "sample": {"skip": True},
            },
            "updated": {
                "marshmallow": {
                    "read": False,
                    "write": False,
                    "field-class": "ma_fields.String",
                    "validators": ["validate_date('%Y-%m-%d')"],
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_date"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "type": "date",
                "facets": {"searchable": True},
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDate"}},
                "sample": {"skip": True},
            },
            "$schema": {
                "marshmallow": {
                    "read": False,
                    "write": False,
                    "field-class": "ma_fields.String",
                    "validators": [],
                    "imports": [],
                },
                "type": "keyword",
                "facets": {"searchable": True},
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "sample": {"skip": True},
            },
        },
        "saved-model-file": "test/models/model.json",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "pid-field-args": ["create=True"],
        "invenio-version-extra-code": "",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "invenio-record-service-extra-code": "",
        "invenio-views-extra-code": "",
        "record-mapping-setup-cfg": "test",
        "index-name": "test-test-1.0.0",
        "record-blueprints-setup-cfg": "test",
        "record-service-class": "test.services.records.service.TestService",
        "record-class": "test.records.api.TestRecord",
        "record-jsonschemas-setup-cfg": "test",
        "config-dummy-class": "test.config.DummyClass",
        "record-resources-package": "test.resources.records",
        "record-resource-blueprint-name": "Test",
        "ext-class": "test.ext.TestExt",
        "flask-extension-name": "test",
        "cli-function": "test.cli.group",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "script-import-sample-data": "data/sample_data.yaml",
        "invenio-ext-extra-code": "",
        "config-package": "test.config",
        "record-api-blueprints-setup-cfg": "test",
        "collection-url": "/test/",
        "service-id": "test",
        "record-service-config-generate-links": True,
        "oarepo-models-setup-cfg": "test",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "pid-field-imports": [
            {"import": "invenio_records_resources.records.systemfields.pid.PIDField"},
            {
                "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
            },
            {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
        ],
        "invenio-record-resource-extra-code": "",
        "record-schema-class": "test.services.records.schema.TestSchema",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "invenio-record-schema-extra-code": "",
        "invenio-record-search-options-extra-code": "",
        "invenio-record-dumper-extra-code": "",
        "generate-record-pid-field": True,
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "pid-field-provider": "RecordIdProviderV2",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "proxies-current-resource": "test.proxies.current_resource",
        "invenio-record-permissions-extra-code": "",
        "record-schema-metadata-alembic": "test",
        "invenio-record-resource-config-extra-code": "",
        "profile-package": "records",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "invenio-config-extra-code": "",
        "record-services-package": "test.services.records",
        "model-name": "test",
        "package-base": "test",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "jsonschemas-package": "test.records.jsonschemas",
        "record-schema-metadata-setup-cfg": "test",
        "invenio-proxies-extra-code": "",
        "pid-field-cls": "PIDField",
        "invenio-record-service-config-extra-code": "",
        "kebap-package": "test",
        "package-path": "test",
        "ui": {
            "marshmallow": {
                "base-classes": ["InvenioUISchema"],
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
                "schema-class": "test.services.records.ui_schema.TestUISchema",
                "generate": True,
            }
        },
        "invenio-record-extra-code": "",
        "pid-field-context": "PIDFieldContext",
        "record-prefix": "Test",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "record-metadata-table-name": "test_metadata",
        "flask-commands-setup-cfg": "test",
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",
        "permissions": {"presets": []},
        "mapping-package": "test.records.mappings",
        "marshmallow": {
            "generate": True,
            "schema-class": "test.services.records.schema.TestSchema",
            "base-classes": ["InvenioBaseRecordSchema"],
        },
        "invenio-record-object-schema-extra-code": "",
        "schema-version": "1.0.0",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
    }
