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
                "properties": {"a": {"type": "flattened"}},
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
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validate as ma_validate
import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
class TestSchema(InvenioBaseRecordSchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Raw()
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
                "a": {"type": "object", "enabled": False},
                "id": {"type": "keyword"},
                "created": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date",
                },
                "updated": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date",
                },
                "$schema": {"type": "keyword"},
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
