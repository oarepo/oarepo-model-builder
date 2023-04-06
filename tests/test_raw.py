import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem


def test_raw_type():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "model": {"use": "invenio", "properties": {"a": {"type": "flattened"}}},
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
from marshmallow import validate as ma_validate
import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.validation import validate_datetime
class TestSchema(InvenioBaseRecordSchema):
    \"""TestSchema schema.\"""
    a = ma_fields.Raw()
    """,
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
                "created": {"type": "date"},
                "updated": {"type": "date"},
                "$schema": {"type": "keyword"},
            },
        }
    }

    data = builder.filesystem.read(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    )
    data = json.loads(data)
    print(data)
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
