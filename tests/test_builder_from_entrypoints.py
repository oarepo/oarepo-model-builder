import json
import os
import re
from pathlib import Path

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from tests.mock_filesystem import MockFilesystem
from tests.utils import assert_python_equals


def test_include_invenio():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "model": {"properties": {"a": {"type": "keyword"}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "schema.py")).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services.records.schema import BaseRecordSchema
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validates as ma_validates

class TestSchema(BaseRecordSchema, ):
    \"""TestSchema schema.\"""
    
    a = ma_fields.String()
    
    created = ma_fields.Date(dump_only=True)
    
    updated = ma_fields.Date(dump_only=True)
    """,
    )

    data = builder.filesystem.read(os.path.join("test", "records", "mappings", "v7", "test", "test-1.0.0.json"))
    data = json.loads(data)
    assert data == {
        "mappings": {
            "properties": {
                "$schema": {"ignore_above": 50, "type": "keyword"},
                "a": {"ignore_above": 50, "type": "keyword"},
                "created": {"type": "date"},
                "id": {"ignore_above": 50, "type": "keyword"},
                "updated": {"type": "date"},
            },
        }
    }


def test_generate_multiple_times():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "model": {"properties": {"a": {"type": "keyword"}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
    snapshot_1 = filesystem.snapshot()

    builder.build(schema, "")
    snapshot_2 = filesystem.snapshot()

    assert snapshot_1 == snapshot_2


def test_incremental_builder():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "model": {"properties": {"a": {"type": "keyword"}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "model": {"properties": {"a": {"type": "keyword"}}}},
        isort=False,
        black=False,
    )

    builder.build(schema, "")
    snapshot_1 = filesystem.snapshot()

    snapshot_1.pop(
        Path.cwd() / "scripts/sample_data.yaml"
    )  # these are always regenerated and random, so do not check them

    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "model": {"properties": {"a": {"type": "keyword"}}}},
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
    snapshot_2 = filesystem.snapshot()

    ret = snapshot_2.pop(
        Path.cwd() / "scripts/sample_data.yaml"
    )  # these are always regenerated and random, so do not check them

    assert set(snapshot_1.keys()) == set(snapshot_2.keys())

    for k, iteration_result in snapshot_1.items():
        expected_result = snapshot_2[k]
        # normally handled by black
        assert_python_equals(iteration_result.replace(",'_id'", ",\n'_id'"), expected_result, f'File {k}')
