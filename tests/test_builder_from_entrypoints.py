import json
import os
import sys
from pathlib import Path

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem
from tests.utils import assert_python_equals

from .utils import strip_whitespaces

OAREPO_USE = "use"


# def test_diff():
#     with open("complex-model/data/sample_data.yaml") as f:
#         sample_data = list(yaml.safe_load_all(f))
#         print(sample_data)
def test_include_invenio():
    schema = load_model(
        "test.yaml",  # NOSONAR
        model_content={
            "version": "1.0.0",
            "record": {
                "module": {"qualified": "test"},
                OAREPO_USE: "invenio",
                "properties": {"a": {"type": "keyword", "required": True}},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ).read()

    assert (
        strip_whitespaces(
            """
import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema



class TestSchema(BaseRecordSchema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.String(required=True)
    """
        )
        == strip_whitespaces(data)
    )

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ).read()
    print(data)
    assert (
        strip_whitespaces(
            """
import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.services.schema.ui import InvenioUISchema
class TestUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.String(required=True)    """
        )
        in strip_whitespaces(data)
    )

    data = builder.filesystem.read(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    )
    data = json.loads(data)
    assert data == {
        "mappings": {
            "properties": {
                "$schema": {"type": "keyword", "ignore_above": 1024},
                "a": {"type": "keyword", "ignore_above": 1024},
                "created": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
                },
                "id": {"type": "keyword", "ignore_above": 1024},
                "pid": {
                    "properties": {
                        "obj_type": {"ignore_above": 1024, "type": "keyword"},
                        "pid_type": {"ignore_above": 1024, "type": "keyword"},
                        "pk": {"type": "integer"},
                        "status": {"ignore_above": 1024, "type": "keyword"},
                    },
                    "type": "object",
                },
                "updated": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
                },
            },
        }
    }

    data = builder.filesystem.read("setup.cfg")
    assert "version = 1.0.0" in data


def test_generate_multiple_times():
    schema = load_model(
        "test.yaml",
        model_content={
            "record": {
                "module": {"qualified": "test"},
                OAREPO_USE: "invenio",
                "properties": {"a": {"type": "keyword"}},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")
    snapshot_1 = filesystem.snapshot()

    # need to reload the schema because of caches ...
    schema = load_model(
        "test.yaml",
        model_content={
            "record": {
                "module": {"qualified": "test"},
                OAREPO_USE: "invenio",
                "properties": {"a": {"type": "keyword"}},
            },
        },
        isort=False,
        black=False,
    )
    builder.build(schema, "record", ["record"], "")
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
        model_content={
            "record": {
                "module": {"qualified": "test"},
                OAREPO_USE: "invenio",
                "properties": {"a": {"type": "keyword"}},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    schema = load_model(
        "test.yaml",
        model_content={
            "record": {
                "module": {"qualified": "test"},
                OAREPO_USE: "invenio",
                "properties": {"a": {"type": "keyword"}},
            },
        },
        isort=False,
        black=False,
    )

    builder.build(schema, "record", ["record"], "")
    snapshot_1 = filesystem.snapshot()

    snapshot_1.pop(
        Path.cwd() / "data/sample_data.yaml"
    )  # these are always regenerated and random, so do not check them

    schema = load_model(
        "test.yaml",
        model_content={
            "record": {
                "module": {"qualified": "test"},
                OAREPO_USE: "invenio",
                "properties": {"a": {"type": "keyword"}},
            },
        },
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")
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
