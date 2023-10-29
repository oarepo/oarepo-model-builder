import json
import os

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

from .utils import strip_whitespaces


def test_raw_type():
    schema = load_model(
        "test.yaml",
        model_content={
            "record": {
                "use": "invenio",
                "properties": {"a": {"type": "flat_object"}},
                "module": {"qualified": "test"},
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
from oarepo_runtime.marshmallow import BaseRecordSchema
class TestSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Dict()
    """
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
                "a": {"type": "flat_object"},
                "id": {"type": "keyword", "ignore_above": 1024},
                "created": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
                },
                "updated": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
                },
                "$schema": {"type": "keyword", "ignore_above": 1024},
            },
        }
    }

    data = builder.filesystem.read(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    )
    data = json.loads(data)
    assert data == {
        "properties": {
            "a": {"type": "object"},
            "id": {"type": "string"},
            "created": {"type": "string", "format": "date-time"},
            "updated": {"type": "string", "format": "date-time"},
            "$schema": {"type": "string"},
        },
        "type": "object",
    }
