import json
import os
import re

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.entrypoints import load_model
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_record_marshmallow import (
    InvenioRecordMarshmallowBuilder,
)
from oarepo_model_builder.model_preprocessors.default_values import (
    DefaultValuesModelPreprocessor,
)
from oarepo_model_builder.model_preprocessors.invenio import InvenioModelPreprocessor
from oarepo_model_builder.model_preprocessors.opensearch import (
    OpensearchModelPreprocessor,
)
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.outputs.python import PythonOutput
from .utils import strip_whitespaces


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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = ModelBuilder(
        output_builders=[
            InvenioRecordMarshmallowBuilder,
            MappingBuilder,
            JSONSchemaBuilder,
        ],
        outputs=[PythonOutput, MappingOutput, JSONSchemaOutput],
        model_preprocessors=[
            DefaultValuesModelPreprocessor,
            OpensearchModelPreprocessor,
            InvenioModelPreprocessor,
        ],
        filesystem=filesystem,
    )

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ).read()
    assert (
        strip_whitespaces(
            """
class TestRecordSchema(InvenioBaseRecordSchema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.String(validate=[ma_validate.OneOf(['a', 'b', 'c'])])
    """
        )
        in strip_whitespaces(data)
    )

    data = builder.filesystem.read(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    )
    data = json.loads(data)
    print(data)
    assert data == {
        "properties": {
            "$schema": {"type": "string"},
            "a": {"type": "string"},
            "created": {"format": "date-time", "type": "string"},
            "id": {"type": "string"},
            "updated": {"format": "date-time", "type": "string"},
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
                "created": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis",
                },
                "id": {"type": "keyword"},
                "updated": {
                    "type": "date",
                    "format": "strict_date_time||strict_date_time_no_millis",
                },
            }
        }
    }
