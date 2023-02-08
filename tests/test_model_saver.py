import json
import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.model_saver import (
    ModelRegistrationBuilder, ModelSaverBuilder)
from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.entrypoints import (
    load_entry_points_dict, load_included_models_from_entry_points)
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.model_preprocessors.default_values import \
    DefaultValuesModelPreprocessor
from oarepo_model_builder.model_preprocessors.invenio import \
    InvenioModelPreprocessor
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.outputs.json import JSONOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.datatype_preprocessor import \
    DataTypePreprocessor
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.validation.model_validation import model_validator
from tests.multilang import (MultilangPreprocessor, MultilingualDataType,
                             UIValidator)

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
    assert data[0] == {
        "model": {
            "type": "object",
            "record-dumper-class": "test.records.dumper.TestDumper",
            "invenio-record-dumper-extra-code": "",
            "schema-version": "1.0.0",
            "record-resource-class": "test.resources.records.resource.TestResource",
            "marshmallow": {
                "schema-class": "test.services.records.schema.TestSchema",  # NOSONAR
                "base-classes": ["ma.Schema"],
                "generate": True,
            },
            "invenio-ext-extra-code": "",
            "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
            "record-mapping-setup-cfg": "test",
            "config-package": "test.config",
            "service-id": "test",
            "mapping-package": "test.records.mappings",
            "record-search-options-class": "test.services.records.search.TestSearchOptions",
            "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
            "invenio-record-permissions-extra-code": "",
            "invenio-record-resource-extra-code": "",
            "index-name": "test-test-1.0.0",
            "generate-record-pid-field": True,
            "record-jsonschemas-setup-cfg": "test",
            "record-facets-class": "test.services.records.facets.Test",
            "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
            "schema-server": "http://localhost/schemas/",
            "record-schema-metadata-setup-cfg": "test",
            "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
            "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
            "record-schema-class": "test.services.records.schema.TestSchema",
            "package-path": "test",
            "record-prefix-snake": "test",
            "script-import-sample-data": "data/sample_data.yaml",
            "ext-class": "test.ext.TestExt",
            "record-service-class": "test.services.records.service.TestService",
            "record-service-config-class": "test.services.records.config.TestServiceConfig",
            "record-dumper-extensions": [],
            "record-resource-blueprint-name": "Test",
            "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
            "invenio-record-resource-config-extra-code": "",
            "jsonschemas-package": "test.records.jsonschemas",
            "package": "test",
            "extension-suffix": "test",
            "saved-model-file": "test/models/model.json",
            "record-schema-metadata-alembic": "test",
            "invenio-record-facets-extra-code": "",
            "record-class": "test.records.api.TestRecord",
            "properties": {
                "a": {
                    "marshmallow": {
                        "field-class": "ma_fields.String",  # NOSONAR
                        "validators": [],
                        "imports": [],
                    },
                    "type": "keyword",
                    "ui": {"class": "bolder"},
                },
                "b": {
                    "marshmallow": {
                        "generate": True,
                        "field-class": "ma_fields.Nested",
                        "validators": [],
                        "schema-class": "test.services.records.schema.BSchema",
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
                            "type": "keyword",
                        }
                    },
                },
                "metadata": {
                    "marshmallow": {
                        "schema-class": "test.services.records.schema.TestMetadataSchema",  # NOSONAR
                        "base-classes": ["ma.Schema"],
                        "generate": True,
                        "field-class": "ma_fields.Nested",
                        "validators": [],
                        "imports": [],
                    },
                    "type": "object",
                    "properties": {},
                },
            },
            "flask-commands-setup-cfg": "test",
            "package-base": "test",
            "record-resources-package": "test.resources.records",
            "oarepo-models-setup-cfg": "test",
            "package-base-upper": "TEST",
            "invenio-record-extra-code": "",
            "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
            "flask-extension-name": "test",
            "invenio-views-extra-code": "",
            "record-records-package": "test.records",
            "record-blueprints-setup-cfg": "test",
            "record-service-config-generate-links": True,
            "invenio-version-extra-code": "",
            "record-metadata-table-name": "test_metadata",
            "invenio-config-extra-code": "",
            "cli-function": "test.cli.group",
            "profile-package": "records",
            "schema-name": "test-1.0.0.json",
            "collection-url": "/test/",
            "invenio-record-search-options-extra-code": "",
            "proxies-current-resource": "test.proxies.current_resource",
            "invenio-proxies-extra-code": "",
            "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
            "record-api-blueprints-setup-cfg": "test",
            "invenio-record-service-config-extra-code": "",
            "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
            "invenio-record-object-schema-extra-code": "",
            "record-metadata-class": "test.records.models.TestMetadata",
            "schema-file": "test/records/jsonschemas/test-1.0.0.json",
            "config-dummy-class": "test.config.DummyClass",
            "kebap-package": "test",
            "model-name": "test",
            "invenio-record-schema-extra-code": "",
            "invenio-record-service-extra-code": "",
            "invenio-record-metadata-extra-code": "",
            "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
            "record-prefix": "Test",
            "proxies-current-service": "test.proxies.current_service",
            "record-services-package": "test.services.records",
        }
    }
    assert data[1].strip() == ""
    assert (
        data[2].strip()
        == """[options.entry_points]
oarepo.models = test = test.models:model.json"""
    )


def build(model, output_builder_components=None, property_preprocessors=None):
    datatypes._prepare_datatypes()
    if UIValidator not in model_validator.validator_map["property"]:
        model_validator.validator_map["property"].append(UIValidator)
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
    assert data[0] == {
        "model": {
            "type": "object",
            "config-dummy-class": "test.config.DummyClass",
            "record-resources-package": "test.resources.records",
            "package-base-upper": "TEST",
            "record-class": "test.records.api.TestRecord",
            "record-resource-class": "test.resources.records.resource.TestResource",
            "invenio-views-extra-code": "",
            "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
            "marshmallow": {
                "schema-class": "test.services.records.schema.TestSchema",
                "generate": True,
                "base-classes": ["InvenioBaseRecordSchema"],
            },
            "package": "test",
            "record-blueprints-setup-cfg": "test",
            "record-schema-class": "test.services.records.schema.TestSchema",
            "record-prefix-snake": "test",
            "record-records-package": "test.records",
            "ext-class": "test.ext.TestExt",
            "invenio-config-extra-code": "",
            "record-services-package": "test.services.records",
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
                    "sample": {"skip": True},
                },
                "created": {
                    "marshmallow": {
                        "write": False,
                        "read": True,
                        "field-class": "ma_fields.String",
                        "validators": ["validate_date('%Y:%m:%d')"],
                        "imports": [
                            {"import": "oarepo_runtime.validation.validate_date"}
                        ],
                    },
                    "type": "date",
                    "sample": {"skip": True},
                },
                "updated": {
                    "marshmallow": {
                        "write": False,
                        "read": True,
                        "field-class": "ma_fields.String",
                        "validators": ["validate_date('%Y:%m:%d')"],
                        "imports": [
                            {"import": "oarepo_runtime.validation.validate_date"}
                        ],
                    },
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
                    "sample": {"skip": True},
                },
            },
            "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
            "record-facets-class": "test.services.records.facets.Test",
            "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
            "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
            "script-import-sample-data": "data/sample_data.yaml",
            "record-service-config-class": "test.services.records.config.TestServiceConfig",
            "invenio-record-extra-code": "",
            "record-dumper-class": "test.records.dumper.TestDumper",
            "jsonschemas-package": "test.records.jsonschemas",
            "record-resource-blueprint-name": "Test",
            "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
            "invenio-record-dumper-extra-code": "",
            "record-dumper-extensions": [],
            "collection-url": "/test/",
            "schema-server": "http://localhost/schemas/",
            "service-id": "test",
            "record-search-options-class": "test.services.records.search.TestSearchOptions",
            "mapping-package": "test.records.mappings",
            "invenio-record-permissions-extra-code": "",
            "model-name": "test",
            "oarepo-models-setup-cfg": "test",
            "invenio-record-object-schema-extra-code": "",
            "schema-name": "test-1.0.0.json",
            "index-name": "test-test-1.0.0",
            "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
            "invenio-version-extra-code": "",
            "package-path": "test",
            "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
            "proxies-current-service": "test.proxies.current_service",
            "invenio-record-resource-config-extra-code": "",
            "package-base": "test",
            "invenio-record-search-options-extra-code": "",
            "invenio-record-service-extra-code": "",
            "invenio-record-resource-extra-code": "",
            "invenio-record-facets-extra-code": "",
            "flask-extension-name": "test",
            "invenio-record-service-config-extra-code": "",
            "saved-model-file": "test/models/model.json",
            "record-schema-metadata-alembic": "test",
            "record-schema-metadata-setup-cfg": "test",
            "invenio-ext-extra-code": "",
            "schema-file": "test/records/jsonschemas/test-1.0.0.json",
            "kebap-package": "test",
            "proxies-current-resource": "test.proxies.current_resource",
            "cli-function": "test.cli.group",
            "record-mapping-setup-cfg": "test",
            "config-package": "test.config",
            "record-service-config-generate-links": True,
            "invenio-record-metadata-extra-code": "",
            "record-prefix": "Test",
            "generate-record-pid-field": True,
            "extension-suffix": "test",
            "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
            "record-jsonschemas-setup-cfg": "test",
            "record-metadata-table-name": "test_metadata",
            "invenio-proxies-extra-code": "",
            "record-metadata-class": "test.records.models.TestMetadata",
            "schema-version": "1.0.0",
            "profile-package": "records",
            "record-api-blueprints-setup-cfg": "test",
            "record-service-class": "test.services.records.service.TestService",
            "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
            "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
            "invenio-record-schema-extra-code": "",
            "flask-commands-setup-cfg": "test",
        }
    }
