import json
import os
import re
import sys
from pathlib import Path

from oarepo_model_builder.entrypoints import (create_builder_from_entrypoints,
                                              load_model)
from oarepo_model_builder.fs import InMemoryFileSystem
from tests.utils import assert_python_equals

OAREPO_USE = "use"


def test_include_invenio():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "version": "1.0.0",
            "model": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validates as ma_validates
import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from oarepo_runtime.validation import validate_date

class TestSchema(InvenioBaseRecordSchema):
    \"""TestSchema schema.\"""
    a = ma_fields.String()
    created = ma_fields.String(validate=[validate_date('%Y:%m:%d')], dump_only=True)
    updated = ma_fields.String(validate=[validate_date('%Y:%m:%d')], dump_only=True)
    """,
    )

    data = builder.filesystem.read(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
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
            "model": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
    snapshot_1 = filesystem.snapshot()

    # need to reload the schema because of caches ...
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "model": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )
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
            "model": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "model": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    builder.build(schema, "")
    snapshot_1 = filesystem.snapshot()

    snapshot_1.pop(
        Path.cwd() / "data/sample_data.yaml"
    )  # these are always regenerated and random, so do not check them

    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "model": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
    snapshot_2 = filesystem.snapshot()

    ret = snapshot_2.pop(
        Path.cwd() / "data/sample_data.yaml"
    )  # these are always regenerated and random, so do not check them

    assert set(snapshot_1.keys()) == set(snapshot_2.keys())

    for k, iteration_result in snapshot_1.items():
        expected_result = snapshot_2[k]
        # normally handled by black
        assert_python_equals(
            iteration_result.replace(",'_id'", ",\n'_id'"), expected_result, f"File {k}"
        )
