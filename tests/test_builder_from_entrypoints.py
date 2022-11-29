import json
import os
import re
import sys
from pathlib import Path

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from tests.mock_filesystem import MockFilesystem
from tests.utils import assert_python_equals

OAREPO_USE = "oarepo:use"


def test_include_invenio():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "version": "1.0.0",
            OAREPO_USE: "invenio",
            "model": {"properties": {"a": {"type": "keyword"}}},
        },
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

    data = builder.filesystem.read(
        os.path.join("test", "records", "mappings", "v2", "test", "test-1.0.0.json")
    )
    data = json.loads(data)
    assert data == {
        "mappings": {
            "properties": {
                "$schema": {"type": "keyword"},
                "a": {"type": "keyword"},
                "created": {"type": "date"},
                "id": {"type": "keyword"},
                "updated": {"type": "date"},
            },
        }
    }

    data = builder.filesystem.read("setup.cfg")
    assert f"version = 1.0.0" in data


def test_generate_multiple_times():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            OAREPO_USE: "invenio",
            "model": {"properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
    snapshot_1 = filesystem.snapshot()

    builder.build(schema, "")
    snapshot_2 = filesystem.snapshot()

    assert snapshot_1.keys() == snapshot_2.keys()

    for k in snapshot_1:
        first_val = snapshot_1[k]
        second_val = snapshot_2[k]
        if first_val != second_val:
            print("ASSERT FAILED", k, file=sys.stderr)
            print("====================", file=sys.stderr)
            print(first_val, file=sys.stderr)
            print("====================", file=sys.stderr)
            print(second_val, file=sys.stderr)
            print("====================", file=sys.stderr)
            assert first_val == second_val


def test_incremental_builder():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            OAREPO_USE: "invenio",
            "model": {"properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            OAREPO_USE: "invenio",
            "model": {"properties": {"a": {"type": "keyword"}}},
        },
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
        model_content={
            OAREPO_USE: "invenio",
            "model": {"properties": {"a": {"type": "keyword"}}},
        },
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
        assert_python_equals(
            iteration_result.replace(",'_id'", ",\n'_id'"), expected_result, f"File {k}"
        )
