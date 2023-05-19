import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.setup_cfg import SetupCfgBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_ext_setup_cfg import InvenioExtSetupCfgBuilder
from oarepo_model_builder.invenio.invenio_record_jsonschemas_setup_cfg import (
    InvenioRecordJSONSchemasSetupCfgBuilder,
)
from oarepo_model_builder.invenio.invenio_record_metadata_alembic_setup_cfg import (
    InvenioRecordMetadataAlembicSetupCfgBuilder,
)
from oarepo_model_builder.invenio.invenio_record_metadata_models_setup_cfg import (
    InvenioRecordMetadataModelsSetupCfgBuilder,
)
from oarepo_model_builder.invenio.invenio_record_resource_setup_cfg import (
    InvenioRecordResourceSetupCfgBuilder,
)
from oarepo_model_builder.invenio.invenio_record_search_setup_cfg import (
    InvenioRecordSearchSetupCfgBuilder,
)
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema

from .utils import strip_whitespaces


def build_python_model(model, output_builders, fn):
    builder = ModelBuilder(
        output_builders=output_builders,
        outputs=[PythonOutput, CFGOutput],
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
                    "opensearch": {"version": "os-v2"},
                },
                "record": {"module": {"qualified": "test"}, **model},
            },
        ),
        profile="record",
        model_path=["record"],
        output_dir="",
    )

    return builder.filesystem.read(fn)


def test_setup_cfg_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [SetupCfgBuilder],
        os.path.join("setup.cfg"),  # NOSONAR
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
[metadata]
name = test
version = 1.0.0
description = Repository model for Test
authors = 


[options]
python = >=3.9
install_requires =
    invenio_access>=1.4.4
    invenio_app>=1.3.4
    invenio_db>=1.0.14
    invenio_pidstore>=1.2.3
    invenio_records>=2.0.0
    invenio-records-rest>=2.1.0
    invenio_records_permissions>=0.13.0
    invenio_records_resources>=0.21.4
    invenio-search>=2.1.0
    tqdm>=4.64.1
    oarepo-runtime>=1.0.0
packages = find:


[options.package_data]
* = *.json, *.rst, *.md, *.json5, *.jinja2
        """
    )


def test_invenio_ext_cfg_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioExtSetupCfgBuilder],
        os.path.join("setup.cfg"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
[options.entry_points]
invenio_base.api_apps = test = test.ext:TestExt
invenio_base.apps = test = test.ext:TestExt        
        """
    )


def test_invenio_jsonschemas_cfg_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordJSONSchemasSetupCfgBuilder],
        os.path.join("setup.cfg"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
[options.entry_points]
invenio_jsonschemas.schemas = test = test.records.jsonschemas      
        """
    )


def test_invenio_model_cfg_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordMetadataModelsSetupCfgBuilder],
        os.path.join("setup.cfg"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
[options.entry_points]
invenio_db.models = test = test.records.models
    
        """
    )


def test_invenio_alembic_cfg_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordMetadataAlembicSetupCfgBuilder],
        os.path.join("setup.cfg"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
[options.entry_points]
invenio_db.alembic = test = test.records:alembic
        """
    )


def test_invenio_resource_cfg_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordResourceSetupCfgBuilder],
        os.path.join("setup.cfg"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
[options.entry_points]
invenio_base.api_blueprints = test = test.views.records.api:create_api_blueprint
invenio_base.blueprints= test= test.views.records.app:create_app_blueprint
        """
    )


def test_invenio_search_cfg_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordSearchSetupCfgBuilder],
        os.path.join("setup.cfg"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
[options.entry_points]
invenio_search.mappings = test = test.records.mappings        
        """
    )
