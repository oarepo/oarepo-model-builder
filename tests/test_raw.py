import json
import os
import re
from pathlib import Path

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from tests.mock_filesystem import MockFilesystem
from tests.utils import assert_python_equals


def test_raw_type():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "model": {"properties": {"a": {"type": "raw"}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "schema.py")).read()

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
import marshmallow.validates as ma_validates
import marshmallow.ValidationError as ma_ValidationError
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema

class TestSchema(ma.Schema, ):
    \"""TestSchema schema.\"""
    
    a = ma_fields.Raw()
    
    id = ma_fields.String()
    
    created = ma_fields.Date()
    
    updated = ma_fields.Date()
    
    _schema = ma_fields.String(data_key='$schema')
    """,
    )

    data = builder.filesystem.read(os.path.join("test", "records", "mappings", "v7", "test", "test-1.0.0.json"))
    data = json.loads(data)

    assert data == {
        "mappings": {
            "properties": {
                "a": {"type": "flatten"},
                "id": {"type": "keyword", "ignore_above": 50},
                "created": {"type": "date"},
                "updated": {"type": "date"},
                "$schema": {"ignore_above": 50, "type": "keyword"}
            },
        }
    }

    data = builder.filesystem.read(os.path.join("test", "records", "jsonschemas", "test-1.0.0.json"))
    data = json.loads(data)
    print(data)
    assert data == {
        "properties": {
            "a": {},
            "id": {"type": "string"},
            "created": {"type": "string", "format": "date"},
            "updated": {"type": "string", "format": "date"},
            "$schema": {"type": "string"}
            },
        "type": "object"
        }
