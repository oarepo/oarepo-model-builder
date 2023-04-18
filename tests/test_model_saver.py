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
        "pid-field-imports": [
            {"import": "invenio_records_resources.records.systemfields.pid.PIDField"},
            {
                "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
            },
            {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
        ],
        "pid-type": "test",
        "record-mapping-setup-cfg": "test",
        "jsonschemas-package": "test.records.jsonschemas",
        "ui": {
            "marshmallow": {
                "base-classes": ["ma.Schema"],
                "schema-class": "test.services.records.ui_schema.TestUISchema",
                "generate": True,
            }
        },
        "record-resource-blueprint-name": "Test",
        "pid-field-cls": "PIDField",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "profile-package": "records",
        "schema-version": "1.0.0",
        "record-prefix-snake": "test",
        "record-dumper-extensions": [],
        "pid-field-provider": "RecordIdProviderV2",
        "record-metadata-table-name": "test_metadata",
        "record-metadata-class": "test.records.models.TestMetadata",
        "record-service-class": "test.services.records.service.TestService",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "config-package": "test.config",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "flask-commands-setup-cfg": "test",
        "invenio-record-service-config-extra-code": "",
        "invenio-record-service-extra-code": "",
        "invenio-record-object-schema-extra-code": "",
        "package": "test",
        "record-api-blueprints-setup-cfg": "test",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "record-service-config-generate-links": True,
        "script-import-sample-data": "data/sample_data.yaml",
        "permissions": {"presets": []},
        "record-jsonschemas-setup-cfg": "test",
        "invenio-config-extra-code": "",
        "record-schema-class": "test.services.records.schema.TestSchema",
        "record-blueprints-setup-cfg": "test",
        "record-class": "test.records.api.TestRecord",
        "record-schema-metadata-alembic": "test",
        "pid-field-args": ["create=True"],
        "pid-field-context": "PIDFieldContext",
        "invenio-record-extra-code": "",
        "invenio-record-dumper-extra-code": "",
        "proxies-current-service": "test.proxies.current_service",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "index-name": "test-test-1.0.0",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "package-path": "test",
        "record-services-package": "test.services.records",
        "flask-extension-name": "test",
        "extension-suffix": "test",
        "record-resources-package": "test.resources.records",
        "generate-record-pid-field": True,
        "package-base-upper": "TEST",
        "model-name": "test",
        "invenio-version-extra-code": "",
        "invenio-proxies-extra-code": "",
        "proxies-current-resource": "test.proxies.current_resource",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "invenio-record-resource-extra-code": "",
        "invenio-record-search-options-extra-code": "",
        "saved-model-file": "test/models/model.json",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "record-service-config-components": [
            "oarepo_runtime.relations.components.CachingRelationsComponent"
        ],
        "record-schema-metadata-setup-cfg": "test",
        "record-pid-provider-class": "test.records.api.TestIdProvider",
        "invenio-record-facets-extra-code": "",
        "service-id": "test",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "kebap-package": "test",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "record-prefix": "Test",
        "collection-url": "/test/",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "invenio-ext-extra-code": "",
        "package-base": "test",
        "mapping-package": "test.records.mappings",
        "invenio-views-extra-code": "",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "ext-class": "test.ext.TestExt",
        "marshmallow": {
            "base-classes": ["ma.Schema"],
            "schema-class": "test.services.records.schema.TestSchema",
            "generate": True,
        },
        "record-resource-class": "test.resources.records.resource.TestResource",
        "invenio-record-permissions-extra-code": "",
        "schema-name": "test-1.0.0.json",
        "config-dummy-class": "test.config.DummyClass",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "invenio-record-metadata-extra-code": "",
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",
        "record-facets-class": "test.services.records.facets.Test",
        "cli-function": "test.cli.group",
        "invenio-record-schema-extra-code": "",
        "oarepo-models-setup-cfg": "test",
        "record-records-package": "test.records",
        "invenio-record-resource-config-extra-code": "",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "properties": {
            "a": {
                "marshmallow": {
                    "validators": [],
                    "field-class": "ma_fields.String",
                    "imports": [],
                },
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "type": "keyword",
            },
            "b": {
                "marshmallow": {
                    "validators": [],
                    "schema-class": "test.services.records.schema.BSchema",
                    "field-class": "ma_fields.Nested",
                    "generate": True,
                    "imports": [],
                },
                "ui": {
                    "marshmallow": {
                        "schema-class": "test.services.records.ui_schema.BUISchema",
                        "field-class": "ma_fields.Nested",
                    }
                },
                "type": "object",
                "properties": {
                    "c": {
                        "marshmallow": {
                            "validators": [],
                            "field-class": "ma_fields.String",
                            "imports": [],
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                        "type": "keyword",
                    }
                },
            },
            "metadata": {
                "marshmallow": {
                    "base-classes": ["ma.Schema"],
                    "validators": [],
                    "schema-class": "test.services.records.schema.TestMetadataSchema",
                    "field-class": "ma_fields.Nested",
                    "generate": True,
                    "imports": [],
                },
                "ui": {
                    "marshmallow": {
                        "base-classes": ["ma.Schema"],
                        "schema-class": "test.services.records.ui_schema.TestMetadataUISchema",
                        "field-class": "ma_fields.Nested",
                        "generate": True,
                    }
                },
                "type": "object",
                "properties": {},
            },
        },
        "schema-server": "local://",
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
        "index-name": "test-test-1.0.0",
        "record-service-config-components": [
            "oarepo_runtime.relations.components.CachingRelationsComponent"
        ],
        "record-services-package": "test.services.records",
        "record-prefix-snake": "test",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "permissions": {"presets": []},
        "pid-type": "test",
        "record-blueprints-setup-cfg": "test",
        "cli-function": "test.cli.group",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "proxies-current-resource": "test.proxies.current_resource",
        "invenio-record-search-options-extra-code": "",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "flask-extension-name": "test",
        "record-resource-blueprint-name": "Test",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "pid-field-cls": "PIDField",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "ui": {
            "marshmallow": {
                "schema-class": "test.services.records.ui_schema.TestUISchema",
                "base-classes": ["InvenioUISchema"],
                "generate": True,
                "imports": [
                    {"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}
                ],
            }
        },
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",
        "schema-name": "test-1.0.0.json",
        "script-import-sample-data": "data/sample_data.yaml",
        "kebap-package": "test",
        "record-api-blueprints-setup-cfg": "test",
        "invenio-record-object-schema-extra-code": "",
        "record-class": "test.records.api.TestRecord",
        "record-service-class": "test.services.records.service.TestService",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "package-base-upper": "TEST",
        "package-base": "test",
        "invenio-record-permissions-extra-code": "",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "properties": {
            "id": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "validators": [],
                    "read": False,
                    "write": False,
                    "imports": [],
                },
                "sample": {"skip": True},
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "type": "keyword",
                "facets": {"searchable": True},
            },
            "created": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "validators": ["validate_datetime"],
                    "read": False,
                    "write": False,
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_datetime"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "sample": {"skip": True},
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDateTime"}},
                "type": "datetime",
                "facets": {"searchable": True},
            },
            "updated": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "validators": ["validate_datetime"],
                    "read": False,
                    "write": False,
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_datetime"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "sample": {"skip": True},
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDateTime"}},
                "type": "datetime",
                "facets": {"searchable": True},
            },
            "$schema": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "validators": [],
                    "read": False,
                    "write": False,
                    "imports": [],
                },
                "sample": {"skip": True},
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "type": "keyword",
                "facets": {"searchable": True},
            },
        },
        "invenio-record-metadata-extra-code": "",
        "invenio-record-extra-code": "",
        "pid-field-provider": "RecordIdProviderV2",
        "profile-package": "records",
        "record-prefix": "Test",
        "pid-field-context": "PIDFieldContext",
        "schema-version": "1.0.0",
        "record-mapping-setup-cfg": "test",
        "marshmallow": {
            "base-classes": ["InvenioBaseRecordSchema"],
            "schema-class": "test.services.records.schema.TestSchema",
            "generate": True,
        },
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "invenio-proxies-extra-code": "",
        "config-package": "test.config",
        "record-jsonschemas-setup-cfg": "test",
        "extension-suffix": "test",
        "record-service-config-generate-links": True,
        "invenio-record-service-config-extra-code": "",
        "config-dummy-class": "test.config.DummyClass",
        "oarepo-models-setup-cfg": "test",
        "invenio-record-facets-extra-code": "",
        "invenio-ext-extra-code": "",
        "record-pid-provider-class": "test.records.api.TestIdProvider",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "collection-url": "/test/",
        "ext-class": "test.ext.TestExt",
        "proxies-current-service": "test.proxies.current_service",
        "record-dumper-extensions": [],
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "pid-field-args": ["create=True"],
        "record-metadata-table-name": "test_metadata",
        "invenio-version-extra-code": "",
        "record-schema-metadata-alembic": "test",
        "invenio-record-service-extra-code": "",
        "package": "test",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "invenio-config-extra-code": "",
        "record-resources-package": "test.resources.records",
        "invenio-record-resource-config-extra-code": "",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "invenio-record-schema-extra-code": "",
        "model-name": "test",
        "service-id": "test",
        "package-path": "test",
        "record-records-package": "test.records",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "record-schema-class": "test.services.records.schema.TestSchema",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "flask-commands-setup-cfg": "test",
        "invenio-views-extra-code": "",
        "pid-field-imports": [
            {"import": "invenio_records_resources.records.systemfields.pid.PIDField"},
            {
                "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
            },
            {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
        ],
        "generate-record-pid-field": True,
        "invenio-record-resource-extra-code": "",
        "record-schema-metadata-setup-cfg": "test",
        "record-facets-class": "test.services.records.facets.Test",
        "saved-model-file": "test/models/model.json",
        "jsonschemas-package": "test.records.jsonschemas",
        "record-metadata-class": "test.records.models.TestMetadata",
        "invenio-record-dumper-extra-code": "",
        "mapping-package": "test.records.mappings",
        "schema-server": "local://",
    }
