import os
import re
import sys

import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_record_resource_config import (
    InvenioRecordResourceConfigBuilder,
)
from oarepo_model_builder.invenio.invenio_record_ui_schema import (
    InvenioRecordUISchemaBuilder,
)
from oarepo_model_builder.invenio.invenio_record_ui_serializer import (
    InvenioRecordUISerializerBuilder,
)
from oarepo_model_builder.model_preprocessors.datatype_default import (
    DatatypeDefaultModelPreprocessor,
)
from oarepo_model_builder.model_preprocessors.default_values import (
    DefaultValuesModelPreprocessor,
)
from oarepo_model_builder.model_preprocessors.invenio import InvenioModelPreprocessor
from oarepo_model_builder.model_preprocessors.opensearch import (
    OpensearchModelPreprocessor,
)
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.datatype_preprocessor import (
    DataTypePreprocessor,
)
from oarepo_model_builder.schema import ModelSchema

OAREPO_MARSHMALLOW = "marshmallow"
B_SCHEMA = 'classB(ma.Schema):"""Bschema."""b=ma_fields.String()'
BUI_SCHEMA = 'classBUISchema(ma.Schema):"""BUISchemaschema."""b=ma_fields.String()'


def get_test_schema(**props):
    return ModelSchema(
        "",
        {
            "settings": {
                "python": {"use-isort": False, "use-black": False},
            },
            "model": {"package": "test", "properties": props},
        },
    )


@pytest.fixture
def fulltext_builder():
    return ModelBuilder(
        output_builders=[
            InvenioRecordUISchemaBuilder,
            InvenioRecordUISerializerBuilder,
            InvenioRecordResourceConfigBuilder,
        ],
        outputs=[PythonOutput],
        model_preprocessors=[
            DefaultValuesModelPreprocessor,
            OpensearchModelPreprocessor,
            InvenioModelPreprocessor,
            DatatypeDefaultModelPreprocessor,
        ],
        property_preprocessors=[DataTypePreprocessor],
    )


def _test(fulltext_builder, string_type):
    schema = get_test_schema(a={"type": string_type})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")  # NOSONAR
    ) as f:
        data = f.read()
    assert "a = ma_fields.String()" in data


def test_fulltext(fulltext_builder):
    _test(fulltext_builder, "fulltext")


def test_keyword(fulltext_builder):
    _test(fulltext_builder, "keyword")


def test_fulltext_keyword(fulltext_builder):
    _test(fulltext_builder, "fulltext+keyword")


def test_simple_array(fulltext_builder):
    schema = get_test_schema(a={"type": "array", "items": {"type": "keyword"}})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert "a = ma_fields.List(ma_fields.String())" in data


def test_array_of_objects(fulltext_builder):
    print("starting test ...", file=sys.stderr)
    schema = get_test_schema(
        a={
            "type": "array",
            "items": {"type": "object", "properties": {"b": {"type": "integer"}}},
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert (
        'class AItemUISchema(ma.Schema):\n    """AItemUISchema schema."""\n    b = ma_fields.Integer()'
        in data
    )
    assert "a = ma_fields.List(ma_fields.Nested(lambda: AItemUISchema()))" in data


def test_generate_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"schema-class": "B", "generate": True},
            "ui": {OAREPO_MARSHMALLOW: {"schema-class": "BUISchema", "generate": True}},
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert (
        re.sub(
            r"\s",
            "",
            """class BUISchema(ma.Schema):
        \"""BUISchema schema.\"""
        
        b = ma_fields.String()""",
        )
        in re.sub(r"\s", "", data)
    )
    assert (
        re.sub(
            r"\s",
            "",
            """class TestUISchema(ma.Schema):
        \"""TestUISchema schema.\"""
        
        a = ma_fields.Nested(lambda: BUISchema())""",
        )
        in re.sub(r"\s", "", data)
    )


def test_generate_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "schema-class": "test.services.schema2.B",
                "generate": True,
            },
            "ui": {
                OAREPO_MARSHMALLOW: {
                    "schema-class": "test.services.schema2.BUISchema",
                    "generate": True,
                }
            },
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestUISchema(ma.Schema):
        \"""TestUISchema schema.\"""
    
        a = ma_fields.Nested(lambda: BUISchema())""",
        )
        in re.sub(r"\s", "", data)
    )


def test_use_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"schema-class": "B", "generate": False},
            "ui": {
                OAREPO_MARSHMALLOW: {"schema-class": "BUISchema", "generate": False}
            },
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
        print(data)
    assert (
        re.sub(
            r"\s",
            "",
            """class TestUISchema(ma.Schema):
        \"""TestUISchema schema.\"""
        
        a = ma_fields.Nested(lambda: BUISchema())""",
        )
        in re.sub(r"\s", "", data)
    )
    assert "classBUISchema(ma.Schema)" not in re.sub(r"\s", "", data)


def test_use_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"schema-class": "c.B", "generate": False},
            "ui": {
                OAREPO_MARSHMALLOW: {"schema-class": "c.BUISchema", "generate": False}
            },
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert re.sub(r"\s", "", "from c import BUISchema") in re.sub(r"\s", "", data)
    assert (
        'classTestUISchema(ma.Schema):"""TestUISchemaschema."""a=ma_fields.Nested(lambda:BUISchema())'
        in re.sub(r"\s", "", data)
    )


def test_generate_nested_schema_array(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "array",
            "items": {
                "type": "object",
                OAREPO_MARSHMALLOW: {"schema-class": "B", "generate": True},
                "ui": {
                    OAREPO_MARSHMALLOW: {"schema-class": "BUISchema", "generate": True}
                },
                "properties": {
                    "b": {
                        "type": "keyword",
                    }
                },
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert BUI_SCHEMA in re.sub(r"\s", "", data)
    assert (
        'classTestUISchema(ma.Schema):"""TestUISchemaschema."""a=ma_fields.List(ma_fields.Nested(lambda:BUISchema()))'
        in re.sub(r"\s", "", data)
    )


def test_extend_existing(fulltext_builder):
    schema = get_test_schema(a={"type": "keyword"}, b={"type": "keyword"})
    fulltext_builder.filesystem = InMemoryFileSystem()

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py"), "w"
    ) as f:
        f.write(
            '''
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
class TestUISchema(ma.Schema):
    """TestUISchema schema."""
    a = ma_fields.String()'''
        )

    fulltext_builder.build(schema, output_dir="")
    data = fulltext_builder.filesystem.read(
        os.path.join("test", "services", "records", "ui_schema.py")
    )
    assert "b = ma_fields.String()" in data


def test_generate_nested_schema_relative_same_package(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "schema-class": ".schema2.B",
                "generate": True,
            },
            "ui": {
                OAREPO_MARSHMALLOW: {
                    "schema-class": ".ui_schema2.BUISchema",
                    "generate": True,
                }
            },
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestUISchema(ma.Schema):
        \"""TestUISchema schema.\"""
    
        a = ma_fields.Nested(lambda:BUISchema())""",
        )
        in re.sub(r"\s", "", data)
    )

    assert "from test.services.records.ui_schema2 import BUISchema" in data
    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema2.py")
    ) as f:
        data = f.read()
    assert BUI_SCHEMA in re.sub(r"\s", "", data)


def test_generate_nested_schema_relative_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "schema-class": ".B",
                "generate": True,
            },
            "ui": {
                OAREPO_MARSHMALLOW: {
                    "schema-class": ".BUISchema",
                    "generate": True,
                }
            },
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestUISchema(ma.Schema):
        \"""TestUISchema schema.\"""

        a = ma_fields.Nested(lambda:BUISchema())""",
        )
        in re.sub(r"\s", "", data)
    )


def test_generate_nested_schema_relative_upper(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "schema-class": "..schema2.B",
                "generate": True,
            },
            "ui": {
                OAREPO_MARSHMALLOW: {
                    "schema-class": "..schema2.BUISchema",
                    "generate": True,
                }
            },
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestUISchema(ma.Schema):
        \"""TestUISchema schema.\"""

        a = ma_fields.Nested(lambda: BUISchema())""",
        )
        in re.sub(r"\s", "", data)
    )

    assert "from test.services.schema2 import BUISchema" in data


def test_generate_json_serializer(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "keyword",
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")
    with fulltext_builder.filesystem.open(
        os.path.join("test", "resources", "records", "ui.py")
    ) as f:
        data = f.read()
        print(data)
    assert (
        re.sub(
            r"\s",
            "",
            """
from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import JSONSerializer

from test.services.records.ui_schema import TestUISchema



class TestUIJSONSerializer(MarshmallowSerializer):
    \"""UI JSON serializer.\"""

    def __init__(self):
        \"""Initialise Serializer.\"""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=TestUISchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui"},
        )    
    """,
        )
        == re.sub(r"\s", "", data)
    )


def test_generate_resource_config(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "keyword",
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")
    with fulltext_builder.filesystem.open(
        os.path.join("test", "resources", "records", "config.py")
    ) as f:
        data = f.read()
        print(data)
    assert (
        re.sub(
            r"\s",
            "",
            """
import importlib_metadata
from flask_resources import ResponseHandler

from test.resources.records.ui import TestUIJSONSerializer



class TestResourceConfig():
    \"""TestRecord resource config.\"""

    blueprint_name = 'Test'
    url_prefix = '/test/'

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(group='invenio.test.response_handlers'):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(TestUIJSONSerializer()),
            **super().response_handlers,
            **entrypoint_response_handlers
        }    """,
        )
        == re.sub(r"\s", "", data)
    )


def test_localized_date(fulltext_builder):
    schema = get_test_schema(a={"type": "date"})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert "a = l10n.LocalizedDate()" in data


def test_metadata(fulltext_builder):
    schema = get_test_schema(
        metadata={"type": "object", "properties": {"a": {"type": "keyword"}}}
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert "metadata = ma_fields.Nested(lambda: TestMetadataUISchema())" in data
