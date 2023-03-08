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
        "cli-function": "test.cli.group",
        "collection-url": "/test/",
        "config-dummy-class": "test.config.DummyClass",
        "config-package": "test.config",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "ext-class": "test.ext.TestExt",
        "extension-suffix": "test",
        "flask-commands-setup-cfg": "test",
        "flask-extension-name": "test",
        "generate-record-pid-field": True,
        "index-name": "test-test-1.0.0",
        "invenio-config-extra-code": "",
        "invenio-ext-extra-code": "",
        "invenio-proxies-extra-code": "",
        "invenio-record-dumper-extra-code": "",
        "invenio-record-extra-code": "",
        "invenio-record-facets-extra-code": "",
        "invenio-record-metadata-extra-code": "",
        "invenio-record-object-schema-extra-code": "",
        "invenio-record-permissions-extra-code": "",
        "invenio-record-resource-config-extra-code": "",
        "invenio-record-resource-extra-code": "",
        "invenio-record-schema-extra-code": "",
        "invenio-record-search-options-extra-code": "",
        "invenio-record-service-config-extra-code": "",
        "invenio-record-service-extra-code": "",
        "invenio-version-extra-code": "",
        "invenio-views-extra-code": "",
        "jsonschemas-package": "test.records.jsonschemas",
        "kebap-package": "test",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "mapping-package": "test.records.mappings",
        "marshmallow": {
            "base-classes": ["ma.Schema"],
            "generate": True,
            "schema-class": "test.services.records.schema.TestSchema",
        },
        "model-name": "test",
        "oarepo-models-setup-cfg": "test",
        "package": "test",
        "package-base": "test",
        "package-base-upper": "TEST",
        "package-path": "test",
        "permissions": {"presets": []},
        "profile-package": "records",
        "properties": {
            "a": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "imports": [],
                    "validators": [],
                },
                "type": "keyword",
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
            },
            "b": {
                "marshmallow": {
                    "field-class": "ma_fields.Nested",
                    "generate": True,
                    "imports": [],
                    "schema-class": "test.services.records.schema.BSchema",
                    "validators": [],
                },
                "properties": {
                    "c": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "imports": [],
                            "validators": [],
                        },
                        "type": "keyword",
                        "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                    }
                },
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "field-class": "ma_fields.Nested",
                        "schema-class": "test.services.records.ui_schema.BUISchema",
                    }
                },
            },
            "metadata": {
                "marshmallow": {
                    "base-classes": ["ma.Schema"],
                    "field-class": "ma_fields.Nested",
                    "generate": True,
                    "imports": [],
                    "schema-class": "test.services.records.schema.TestMetadataSchema",
                    "validators": [],
                },
                "properties": {},
                "type": "object",
                "ui": {
                    "marshmallow": {
                        "base-classes": ["ma.Schema"],
                        "field-class": "ma_fields.Nested",
                        "generate": True,
                        "schema-class": "test.services.records.ui_schema.TestMetadataUISchema",
                    }
                },
            },
        },
        "proxies-current-resource": "test.proxies.current_resource",
        "proxies-current-service": "test.proxies.current_service",
        "record-api-blueprints-setup-cfg": "test",
        "record-blueprints-setup-cfg": "test",
        "record-class": "test.records.api.TestRecord",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "record-dumper-extensions": [],
        "record-facets-class": "test.services.records.facets.Test",
        "record-jsonschemas-setup-cfg": "test",
        "record-mapping-setup-cfg": "test",
        "record-metadata-class": "test.records.models.TestMetadata",
        "record-metadata-table-name": "test_metadata",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "record-prefix": "Test",
        "record-prefix-snake": "test",
        "record-records-package": "test.records",
        "record-resource-blueprint-name": "Test",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "record-resources-package": "test.resources.records",
        "record-schema-class": "test.services.records.schema.TestSchema",
        "record-schema-metadata-alembic": "test",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "record-schema-metadata-setup-cfg": "test",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "record-service-class": "test.services.records.service.TestService",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "record-service-config-generate-links": True,
        "record-services-package": "test.services.records",
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "saved-model-file": "test/models/model.json",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "schema-name": "test-1.0.0.json",
        "schema-server": "http://localhost/schemas/",
        "schema-version": "1.0.0",
        "script-import-sample-data": "data/sample_data.yaml",
        "service-id": "test",
        "type": "object",
        "ui": {
            "marshmallow": {
                "base-classes": ["ma.Schema"],
                "generate": True,
                "schema-class": "test.services.records.ui_schema.TestUISchema",
            }
        },
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
        "record-resource-class": "test.resources.records.resource.TestResource",
        "marshmallow": {
            "schema-class": "test.services.records.schema.TestSchema",
            "base-classes": ["InvenioBaseRecordSchema"],
            "generate": True,
        },
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "properties": {
            "id": {
                "marshmallow": {
                    "read": False,
                    "validators": [],
                    "field-class": "ma_fields.String",
                    "write": False,
                    "imports": [],
                },
                "facets": {"searchable": True},
                "type": "keyword",
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "sample": {"skip": True},
            },
            "created": {
                "marshmallow": {
                    "read": True,
                    "validators": ["validate_date('%Y-%m-%d')"],
                    "field-class": "ma_fields.String",
                    "write": False,
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_date"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "facets": {"searchable": True},
                "type": "date",
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDate"}},
                "sample": {"skip": True},
            },
            "updated": {
                "marshmallow": {
                    "read": True,
                    "validators": ["validate_date('%Y-%m-%d')"],
                    "field-class": "ma_fields.String",
                    "write": False,
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_date"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "facets": {"searchable": True},
                "type": "date",
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDate"}},
                "sample": {"skip": True},
            },
            "$schema": {
                "marshmallow": {
                    "read": False,
                    "validators": [],
                    "field-class": "ma_fields.String",
                    "write": False,
                    "imports": [],
                },
                "facets": {"searchable": True},
                "type": "keyword",
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "sample": {"skip": True},
            },
        },
        "record-mapping-setup-cfg": "test",
        "invenio-record-metadata-extra-code": "",
        "invenio-record-service-extra-code": "",
        "mapping-package": "test.records.mappings",
        "record-service-config-generate-links": True,
        "invenio-record-search-options-extra-code": "",
        "extension-suffix": "test",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "oarepo-models-setup-cfg": "test",
        "record-class": "test.records.api.TestRecord",
        "invenio-record-service-config-extra-code": "",
        "saved-model-file": "test/models/model.json",
        "record-resources-package": "test.resources.records",
        "collection-url": "/test/",
        "config-dummy-class": "test.config.DummyClass",
        "invenio-version-extra-code": "",
        "invenio-proxies-extra-code": "",
        "model-name": "test",
        "record-services-package": "test.services.records",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "record-facets-class": "test.services.records.facets.Test",
        "record-metadata-table-name": "test_metadata",
        "invenio-config-extra-code": "",
        "ext-class": "test.ext.TestExt",
        "schema-name": "test-1.0.0.json",
        "record-blueprints-setup-cfg": "test",
        "proxies-current-service": "test.proxies.current_service",
        "proxies-current-resource": "test.proxies.current_resource",
        "package-base": "test",
        "invenio-record-dumper-extra-code": "",
        "schema-version": "1.0.0",
        "invenio-record-resource-config-extra-code": "",
        "record-prefix": "Test",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "index-name": "test-test-1.0.0",
        "invenio-views-extra-code": "",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "record-schema-metadata-alembic": "test",
        "package-path": "test",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "kebap-package": "test",
        "profile-package": "records",
        "flask-extension-name": "test",
        "invenio-record-schema-extra-code": "",
        "record-jsonschemas-setup-cfg": "test",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
        "schema-server": "http://localhost/schemas/",
        "record-dumper-extensions": [],
        "invenio-record-permissions-extra-code": "",
        "flask-commands-setup-cfg": "test",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "record-resource-blueprint-name": "Test",
        "record-schema-metadata-setup-cfg": "test",
        "service-id": "test",
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",
        "record-ui-schema-metadata-class": "test.services.records.ui_schema.TestMetadataUISchema",
        "record-api-blueprints-setup-cfg": "test",
        "ui": {
            "marshmallow": {
                "schema-class": "test.services.records.ui_schema.TestUISchema",
                "base-classes": ["ma.Schema"],
                "generate": True,
            }
        },
        "record-dumper-class": "test.records.dumper.TestDumper",
        "package-base-upper": "TEST",
        "invenio-record-resource-extra-code": "",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "record-metadata-class": "test.records.models.TestMetadata",
        "jsonschemas-package": "test.records.jsonschemas",
        "invenio-record-facets-extra-code": "",
        "script-import-sample-data": "data/sample_data.yaml",
        "invenio-record-extra-code": "",
        "config-package": "test.config",
        "record-schema-class": "test.services.records.schema.TestSchema",
        "cli-function": "test.cli.group",
        "invenio-ext-extra-code": "",
        "record-records-package": "test.records",
        "invenio-record-object-schema-extra-code": "",
        "package": "test",
        "permissions": {"presets": []},
        "generate-record-pid-field": True,
        "record-service-class": "test.services.records.service.TestService",
        "record-prefix-snake": "test",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
    }
