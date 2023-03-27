import json
import os
import re

import yaml

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem


def test_array_shortcuts():
    schema = load_model(
        "test.yaml",  # NOSONAR
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {"a[]": {"type": "keyword", "^required": True}},
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
    a = ma_fields.List(ma_fields.String())        
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
            }
        }
    }

    data = builder.filesystem.read(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    )
    data = json.loads(data)
    assert data == {
        "properties": {
            "$schema": {"type": "string"},
            "a": {"items": {"type": "string"}, "type": "array"},
            "created": {"format": "date", "type": "string"},
            "id": {"type": "string"},
            "updated": {"format": "date", "type": "string"},
        },
        "type": "object",
    }


def test_singleline_type_shortcut():
    data = """
model:
  properties:
    metadata:
      properties:
        title: fulltext
"""

    schema = load_model(
        "test.yaml",
        "test",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")


def test_object_shortcut():
    data = """
model:
  properties:
    metadata{}:
      title: fulltext
"""

    schema = load_model(
        "test.yaml",
        "test",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")


def test_array_shortcut():
    data = """
model:
  properties:
    metadata[]:
      type: fulltext
"""

    schema = load_model(
        "test.yaml",
        "test",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")


def test_array_single_line_shortcut():
    data = """
model:
  properties:
    metadata[]: fulltext
"""

    schema = load_model(
        "test.yaml",
        "test",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")


def test_misc_shortcuts():
    data = """
model:
  properties:
    metadata:
      properties:
        title: fulltext
"""
    """
      description: fulltext+keyword
      kind: keyword{enum:[article, dataset]}
      printed{}:
      ^marshmallow:
        schema-class: PrintedPublicationSchema
      price: double{minimumExclusive:0}
      floatPrice: float     # just to test floats
      published: date
      "sources{nested}[]":
        source: fulltext
        period: edtf-interval
"""

    schema = load_model(
        "test.yaml",
        "test",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
