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
    
    a = ma_fields.Raw()
    
    created = ma_fields.Date(dump_only=True)
    
    updated = ma_fields.Date(dump_only=True)

    """,
    )

    data = builder.filesystem.read(os.path.join("test", "records", "mappings", "v7", "test", "test-1.0.0.json"))
    data = json.loads(data)

    assert data == {
        "mappings": {
            "properties": {
                "a": {"type": "flatten"},
                "id": {"type": "keyword"},
                "created": {"type": "date"},
                "updated": {"type": "date"},
                "$schema": {"type": "keyword"}
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
