import json
import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.model_saver import (
    ModelRegistrationBuilder,
    ModelSaverBuilder,
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
from tests.mock_filesystem import MockFilesystem

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
        "type": "object",
        "properties": {
            "a": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
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
                "properties": {},
                "marshmallow": {
                    "schema-class": "test.services.records.schema.TestMetadataSchema",
                    "base-classes": ["ma.Schema"],
                    "generate": True,
                },
            },
        },
        "package": "test",
        "record-prefix": "Test",
        "package-base": "test",
        "package-base-upper": "TEST",
        "kebap-package": "test",
        "package-path": "test",
        "schema-version": "1.0.0",
        "schema-name": "test-1.0.0.json",
        "schema-file": "test/records/jsonschemas/test-1.0.0.json",
        "mapping-package": "test.records.mappings",
        "jsonschemas-package": "test.records.jsonschemas",
        "mapping-file": "test/records/mappings/os-v2/test/test-1.0.0.json",
        "schema-server": "http://localhost/schemas/",
        "index-name": "test-test-1.0.0",
        "collection-url": "/test/",
        "model-name": "test",
        "saved-model-file": "test/models/model.json",
        "marshmallow": {
            "mapping": {},
            "schema-class": "test.services.records.schema.TestSchema",
            "base-classes": ["ma.Schema"],
            "generate": True,
        },
        "extension-suffix": "test",
        "profile-package": "records",
        "record-prefix-snake": "test",
        "record-resources-package": "test.resources.records",
        "record-services-package": "test.services.records",
        "record-records-package": "test.records",
        "config-package": "test.config",
        "config-dummy-class": "test.config.DummyClass",
        "config-resource-config-key": "TEST_RESOURCE_CONFIG_TEST",
        "config-resource-class-key": "TEST_RESOURCE_CLASS_TEST",
        "config-service-config-key": "TEST_SERVICE_CONFIG_TEST",
        "config-service-class-key": "TEST_SERVICE_CLASS_TEST",
        "config-resource-register-blueprint-key": "TEST_REGISTER_BLUEPRINT",
        "ext-class": "test.ext.TestExt",
        "flask-extension-name": "test",
        "cli-function": "test.cli.group",
        "proxies-current-resource": "test.proxies.current_resource",
        "proxies-current-service": "test.proxies.current_service",
        "record-class": "test.records.api.TestRecord",
        "record-metadata-class": "test.records.models.TestMetadata",
        "record-metadata-table-name": "test_metadata",
        "record-mapping-setup-cfg": "test",
        "record-jsonschemas-setup-cfg": "test",
        "record-resource-config-class": "test.resources.records.config.TestResourceConfig",
        "record-resource-class": "test.resources.records.resource.TestResource",
        "record-permissions-class": "test.services.records.permissions.TestPermissionPolicy",
        "record-service-class": "test.services.records.service.TestService",
        "record-service-config-class": "test.services.records.config.TestServiceConfig",
        "record-service-config-generate-links": True,
        "record-schema-class": "test.services.records.schema.TestSchema",
        "record-schema-metadata-class": "test.services.records.schema.TestMetadataSchema",
        "record-dumper-class": "test.records.dumper.TestDumper",
        "record-search-options-class": "test.services.records.search.TestSearchOptions",
        "record-facets-class": "test.services.records.facets.Test",
        "record-schema-metadata-alembic": "test",
        "record-schema-metadata-setup-cfg": "test",
        "record-resource-blueprint-name": "Test",
        "create-blueprint-from-app": "test.views.create_blueprint_from_app_test",
        "invenio-config-extra-code": "",
        "invenio-ext-extra-code": "",
        "invenio-proxies-extra-code": "",
        "invenio-record-extra-code": "",
        "invenio-record-dumper-extra-code": "",
        "invenio-record-facets-extra-code": "",
        "invenio-record-metadata-extra-code": "",
        "invenio-record-object-schema-extra-code": "",
        "invenio-record-permissions-extra-code": "",
        "invenio-record-resource-extra-code": "",
        "invenio-record-resource-config-extra-code": "",
        "invenio-record-schema-extra-code": "",
        "invenio-record-search-options-extra-code": "",
        "invenio-record-service-extra-code": "",
        "invenio-record-service-config-extra-code": "",
        "invenio-version-extra-code": "",
        "invenio-views-extra-code": "",
        "generate-record-pid-field": True,
        "record-dumper-extensions": [],
        "script-import-sample-data": "data/sample_data.yaml",
        "service-id": "test",
    }

    assert data[1].strip() == ""
    assert (
        data[2].strip()
        == """[options.entry_points]
oarepo.models = test = test.models:model.json"""
    )


def build(model, output_builder_components=None, property_preprocessors=None):
    builder = ModelBuilder(
        output_builders=[
            ModelSaverBuilder,
            ModelRegistrationBuilder,
        ],
        outputs=[JSONOutput, PythonOutput, CFGOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor, InvenioModelPreprocessor],
        output_builder_components=output_builder_components,
        filesystem=MockFilesystem(),
        property_preprocessors=property_preprocessors,
        included_validation_schemas=[
            {
                "jsonschema-property": {
                    "properties": {
                        "type": {"enum": ["multilingual"]},
                        "ui": {"type": "object", "additionalProperties": True},
                    }
                }
            }
        ],
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {
                        "use_isort": False,
                        "use_black": False,
                    },
                },
                "model": {
                    **model,
                    "package": "test",
                    "record-prefix": "Test",
                },
            },
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
