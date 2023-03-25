import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem


def test_enum():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {"a": {"type": "keyword", "enum": ["a", "b", "c"]}},
            },
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
from oarepo_runtime.validation import validate_date

class TestSchema(InvenioBaseRecordSchema):
    \"""TestSchema schema.\"""
    
    a = ma_fields.String(validate=[ma_validate.OneOf(["a", "b", "c"])])
""",
    )

    data = builder.filesystem.read(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    )
    data = json.loads(data)
    print(data)
    assert data == {
        "properties": {
            "$schema": {"type": "string"},
            "a": {"type": "string", "enum": ["a", "b", "c"]},
            "created": {"format": "date", "type": "string"},
            "id": {"type": "string"},
            "updated": {"format": "date", "type": "string"},
        },
        "type": "object",
    }

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
            }
        }
    }
