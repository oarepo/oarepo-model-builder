import json
import os
import re
from pathlib import Path

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from tests.mock_filesystem import MockFilesystem
from tests.utils import assert_python_equals


def test_array_shortcuts():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "oarepo:use": "invenio",
            "model": {"properties": {"a[]": {"type": "keyword", "required[]": True}}},
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
    
    created = ma_fields.Date(dump_only=True)
    
    updated = ma_fields.Date(dump_only=True)
    
    a = ma_fields.List(ma_fields.String())
        """,
    )

    data = builder.filesystem.read(os.path.join("test", "records", "mappings", "v7", "test", "test-1.0.0.json"))
    data = json.loads(data)
    assert data == {
        "mappings": {
            "properties": {
                "$schema": {"ignore_above": 50, "type": "keyword"},
                "a": {
                    "ignore_above": 50,
                    "type": "keyword",
                },
                "created": {"type": "date"},
                "id": {"ignore_above": 50, "type": "keyword"},
                "updated": {"type": "date"},
            }
        }
    }

    data = builder.filesystem.read(os.path.join("test", "records", "jsonschemas", "test-1.0.0.json"))
    data = json.loads(data)
    assert data == {
        "properties": {
            "$schema": {"type": "string"},
            "a": {"items": {"type": "string"}, "type": "array"},
            "created": {"format": "date", "type": "string"},
            "id": {"type": "string"},
            "updated": {"format": "date", "type": "string"},
        },
        "required": ["a"],
        "type": "object",
    }
