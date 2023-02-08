import os
import re

import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_record_schema import \
    InvenioRecordSchemaBuilder
from oarepo_model_builder.model_preprocessors.default_values import \
    DefaultValuesModelPreprocessor
from oarepo_model_builder.model_preprocessors.invenio import \
    InvenioModelPreprocessor
from oarepo_model_builder.model_preprocessors.opensearch import \
    OpensearchModelPreprocessor
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.datatype_preprocessor import \
    DataTypePreprocessor
from oarepo_model_builder.schema import ModelSchema

OAREPO_MARSHMALLOW = "marshmallow"
B_SCHEMA = 'classB(ma.Schema):"""Bschema."""b=ma_fields.String()'


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
        output_builders=[InvenioRecordSchemaBuilder],
        outputs=[PythonOutput],
        model_preprocessors=[
            DefaultValuesModelPreprocessor,
            OpensearchModelPreprocessor,
            InvenioModelPreprocessor,
        ],
        property_preprocessors=[DataTypePreprocessor],
    )


def _test(fulltext_builder, string_type):
    schema = get_test_schema(a={"type": string_type})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert "a = ma_fields.List(ma_fields.String())" in data


def test_array_of_objects(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "array",
            "items": {"type": "object", "properties": {"b": {"type": "integer"}}},
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(schema, output_dir="")

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        'class AItemSchema(ma.Schema):\n    """AItemSchema schema."""\n    b = ma_fields.Integer()'
        in data
    )
    assert "a = ma_fields.List(ma_fields.Nested(lambda: AItemSchema()))" in data


def test_generate_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"schema-class": "B", "generate": True},
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        re.sub(
            r"\s",
            "",
            """class B(ma.Schema):
        \"""B schema.\"""
        
        b = ma_fields.String()""",
        )
        in re.sub(r"\s", "", data)
    )
    assert (
        re.sub(
            r"\s",
            "",
            """class TestSchema(ma.Schema):
        \"""TestSchema schema.\"""
        
        a = ma_fields.Nested(lambda: B())""",
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestSchema(ma.Schema):
        \"""TestSchema schema.\"""
    
        a = ma_fields.Nested(lambda: B())""",
        )
        in re.sub(r"\s", "", data)
    )

    assert "from test.services.schema2 import B" in data

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "schema2.py")
    ) as f:
        data = f.read()
    assert B_SCHEMA in re.sub(r"\s", "", data)


def test_use_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"schema-class": "B", "generate": False},
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
        print(data)
    assert (
        re.sub(
            r"\s",
            "",
            """class TestSchema(ma.Schema):
        \"""TestSchema schema.\"""
        
        a = ma_fields.Nested(lambda: B())""",
        )
        in re.sub(r"\s", "", data)
    )
    assert "classB(ma.Schema)" not in re.sub(r"\s", "", data)


def test_use_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"schema-class": "c.B", "generate": False},
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert re.sub(r"\s", "", "from c import B") in re.sub(r"\s", "", data)
    assert (
        'classTestSchema(ma.Schema):"""TestSchemaschema."""a=ma_fields.Nested(lambda:B())'
        in re.sub(r"\s", "", data)
    )


def test_generate_nested_schema_array(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "array",
            "items": {
                "type": "object",
                OAREPO_MARSHMALLOW: {"schema-class": "B", "generate": True},
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert B_SCHEMA in re.sub(r"\s", "", data)
    assert (
        'classTestSchema(ma.Schema):"""TestSchemaschema."""a=ma_fields.List(ma_fields.Nested(lambda:B()))'
        in re.sub(r"\s", "", data)
    )


def test_extend_existing(fulltext_builder):
    schema = get_test_schema(a={"type": "keyword"}, b={"type": "keyword"})
    fulltext_builder.filesystem = InMemoryFileSystem()

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py"), "w"
    ) as f:
        f.write(
            '''
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
class TestSchema(ma.Schema):
    """TestSchema schema."""
    a = ma_fields.String()'''
        )

    fulltext_builder.build(schema, output_dir="")
    data = fulltext_builder.filesystem.read(
        os.path.join("test", "services", "records", "schema.py")
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestSchema(ma.Schema):
        \"""TestSchema schema.\"""
    
        a = ma_fields.Nested(lambda:B())""",
        )
        in re.sub(r"\s", "", data)
    )

    assert "from test.services.records.schema2 import B" in data

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema2.py")
    ) as f:
        data = f.read()
    assert B_SCHEMA in re.sub(r"\s", "", data)


def test_generate_nested_schema_relative_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "schema-class": ".B",
                "generate": True,
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestSchema(ma.Schema):
        \"""TestSchema schema.\"""

        a = ma_fields.Nested(lambda:B())""",
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
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        re.sub(
            r"\s",
            "",
            """class TestSchema(ma.Schema):
        \"""TestSchema schema.\"""

        a = ma_fields.Nested(lambda: B())""",
        )
        in re.sub(r"\s", "", data)
    )

    assert "from test.services.schema2 import B" in data

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "schema2.py")
    ) as f:
        data = f.read()
    assert B_SCHEMA in re.sub(r"\s", "", data)
