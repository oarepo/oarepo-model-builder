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
    print(json.dumps(data[0]))
    assert data[0]["model"] == {
        "type": "object",
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",  # NOSONAR
        "record-dumper-extensions": [],
        "schema-name": "test-1.0.0.json",
        "flask-extension-name": "test",
        "flask-commands-setup-cfg": "test",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "invenio-record-service-config-extra-code": "",
        "package-base-upper": "TEST",
        "invenio-record-extra-code": "",
        "ext-class": "test.ext.TestExt",
        "kebap-package": "test",
        "record-records-package": "test.records",
        "record-service-class": "test.services.records.service.TestService",
        "collection-url": "/test/",
        "invenio-record-facets-extra-code": "",
        "invenio-record-permissions-extra-code": "",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "invenio-record-schema-extra-code": "",
        "marshmallow": {
            "schema-class": "test.services.records.schema.TestSchema",  # NOSONAR
            "generate": True,
            "base-classes": ["ma.Schema"],
        },
        "record-api-blueprints-setup-cfg": "test",
        "properties": {
            "a": {
                "marshmallow": {
                    "field-class": "ma_fields.String",  # NOSONAR
                    "validators": [],
                    "imports": [],
                },
                "type": "keyword",
                "ui": {},
            },
            "b": {
                "marshmallow": {
                    "generate": True,
                    "field-class": "ma_fields.Nested",
                    "validators": [],
                    "schema-class": "test.services.records.schema.BSchema",
                    "imports": [],
                },
                "properties": {
                    "c": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [],
                            "imports": [],
                        },
                        "type": "keyword",
                    }
                },
                "type": "object",
            },
            "metadata": {
                "marshmallow": {
                    "schema-class": "test.services.records.schema.TestMetadataSchema",  # NOSONAR
                    "generate": True,
                    "base-classes": ["ma.Schema"],
                    "field-class": "ma_fields.Nested",
                    "validators": [],
                    "imports": [],
                },
                "properties": {},
                "type": "object",
            },
        },
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "invenio-ext-extra-code": "",
        "record-prefix": "Test",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "record-schema-metadata-alembic": "test",
        "invenio-record-resource-extra-code": "",
        "proxies-current-service": "test.proxies.current_service",
        "invenio-record-metadata-extra-code": "",
        "record-metadata-class": "test.records.models.TestMetadata",
        "invenio-version-extra-code": "",
        "schema-server": "http://localhost/schemas/",
        "package-base": "test",
        "record-blueprints-setup-cfg": "test",
        "jsonschemas-package": "test.records.jsonschemas",
        "record-metadata-table-name": "test_metadata",
        "model-name": "test",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "record-jsonschemas-setup-cfg": "test",
        "invenio-record-object-schema-extra-code": "",
        "oarepo-models-setup-cfg": "test",
        "config-package": "test.config",
        "invenio-record-dumper-extra-code": "",
        "ui": {
            "marshmallow": {
                "schema-class": "test.services.records.ui_schema.TestUISchema",  # NOSONAR
                "generate": True,
                "base-classes": ["BaseObjectSchema"],
            }
        },
        "record-services-package": "test.services.records",
        "generate-record-pid-field": True,
        "invenio-record-search-options-extra-code": "",
        "record-facets-class": "test.services.records.facets.Test",
        "proxies-current-resource": "test.proxies.current_resource",
        "invenio-views-extra-code": "",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "package": "test",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "invenio-config-extra-code": "",
        "record-service-config-generate-links": True,
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "record-class": "test.records.api.TestRecord",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "record-resources-package": "test.resources.records",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "record-schema-class": "test.services.records.schema.TestSchema",
        "invenio-record-resource-config-extra-code": "",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "extension-suffix": "test",
        "package-path": "test",
        "permissions": {"presets": []},
        "index-name": "test-test-1.0.0",
        "service-id": "test",
        "config-dummy-class": "test.config.DummyClass",
        "schema-version": "1.0.0",
        "script-import-sample-data": "data/sample_data.yaml",
        "saved-model-file": "test/models/model.json",
        "invenio-record-service-extra-code": "",
        "profile-package": "records",
        "invenio-proxies-extra-code": "",
        "record-resource-blueprint-name": "Test",
        "mapping-package": "test.records.mappings",
        "record-schema-metadata-setup-cfg": "test",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "record-prefix-snake": "test",
        "cli-function": "test.cli.group",
        "record-mapping-setup-cfg": "test",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
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
        model_preprocessors=[DefaultValuesModelPreprocessor, InvenioModelPreprocessor],
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
        "flask-extension-name": "test",
        "record-api-blueprints-setup-cfg": "test",
        "schema-name": "test-1.0.0.json",
        "ui": {
            "marshmallow": {
                "base-classes": ["BaseObjectSchema"],
                "schema-class": "test.services.records.ui_schema.TestUISchema",  # NOSONAR
                "generate": True,
            }
        },
        "proxies-current-service": "test.proxies.current_service",
        "flask-commands-setup-cfg": "test",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "invenio-version-extra-code": "",
        "record-ui-schema-class": "test.services.records.ui_schema.TestUISchema",  # NOSOONAR
        "index-name": "test-test-1.0.0",
        "schema-server": "http://localhost/schemas/",
        "service-id": "test",
        "invenio-record-resource-config-extra-code": "",
        "config-dummy-class": "test.config.DummyClass",
        "kebap-package": "test",
        "saved-model-file": "test/models/model.json",
        "record-metadata-table-name": "test_metadata",
        "invenio-record-metadata-extra-code": "",
        "package-path": "test",
        "record-dumper-extensions": [],
        "oarepo-models-setup-cfg": "test",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "record-resource-blueprint-name": "Test",
        "record-class": "test.records.api.TestRecord",
        "invenio-proxies-extra-code": "",
        "package": "test",
        "invenio-record-service-extra-code": "",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "invenio-record-extra-code": "",
        "record-prefix": "Test",
        "invenio-record-permissions-extra-code": "",
        "schema-version": "1.0.0",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "invenio-record-service-config-extra-code": "",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "collection-url": "/test/",
        "record-jsonschemas-setup-cfg": "test",
        "invenio-record-facets-extra-code": "",
        "ext-class": "test.ext.TestExt",
        "record-schema-class": "test.services.records.schema.TestSchema",
        "package-base-upper": "TEST",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "record-resources-package": "test.resources.records",
        "invenio-ext-extra-code": "",
        "profile-package": "records",
        "record-records-package": "test.records",
        "extension-suffix": "test",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "record-schema-metadata-setup-cfg": "test",
        "proxies-current-resource": "test.proxies.current_resource",
        "permissions": {"presets": []},
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "jsonschemas-package": "test.records.jsonschemas",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "record-schema-metadata-alembic": "test",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "marshmallow": {
            "base-classes": ["InvenioBaseRecordSchema"],
            "schema-class": "test.services.records.schema.TestSchema",
            "generate": True,
        },
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "record-service-class": "test.services.records.service.TestService",
        "properties": {
            "id": {
                "marshmallow": {
                    "write": False,
                    "read": False,
                    "field-class": "ma_fields.String",
                    "validators": [],
                    "imports": [],
                },
                "type": "keyword",
                "facets": {"searchable": True},
                "sample": {"skip": True},
            },
            "created": {
                "marshmallow": {
                    "write": False,
                    "read": True,
                    "field-class": "ma_fields.String",
                    "validators": ["validate_date('%Y-%m-%d')"],
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_date"},
                        {"import": "oarepo_ui.marshmallow.LocalizedDate"},
                    ],
                },
                "facets": {"searchable": True},
                "type": "date",
                "sample": {"skip": True},
            },
            "updated": {
                "marshmallow": {
                    "write": False,
                    "read": True,
                    "field-class": "ma_fields.String",
                    "validators": ["validate_date('%Y-%m-%d')"],
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_date"},
                        {"import": "oarepo_ui.marshmallow.LocalizedDate"},
                    ],
                },
                "facets": {"searchable": True},
                "type": "date",
                "sample": {"skip": True},
            },
            "$schema": {
                "marshmallow": {
                    "write": False,
                    "read": False,
                    "field-class": "ma_fields.String",
                    "validators": [],
                    "imports": [],
                },
                "type": "keyword",
                "facets": {"searchable": True},
                "sample": {"skip": True},
            },
        },
        "invenio-views-extra-code": "",
        "model-name": "test",
        "invenio-record-search-options-extra-code": "",
        "record-blueprints-setup-cfg": "test",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "script-import-sample-data": "data/sample_data.yaml",
        "cli-function": "test.cli.group",
        "record-metadata-class": "test.records.models.TestMetadata",
        "record-facets-class": "test.services.records.facets.Test",
        "invenio-record-resource-extra-code": "",
        "invenio-record-dumper-extra-code": "",
        "mapping-package": "test.records.mappings",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "invenio-record-object-schema-extra-code": "",
        "config-package": "test.config",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "package-base": "test",
        "record-service-config-generate-links": True,
        "invenio-config-extra-code": "",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "generate-record-pid-field": True,
        "record-mapping-setup-cfg": "test",
        "record-prefix-snake": "test",
        "record-services-package": "test.services.records",
        "invenio-record-schema-extra-code": "",
        "record-ui-serializer-class": "test.resources.records.ui.TestUIJSONSerializer",
    }
