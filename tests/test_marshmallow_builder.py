import os

import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_record_marshmallow import (
    InvenioRecordMarshmallowBuilder,
)
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema

from .utils import strip_whitespaces

OAREPO_MARSHMALLOW = "marshmallow"


def get_test_schema(**props):
    return ModelSchema(
        "",
        {
            "settings": {
                "python": {
                    "use-isort": False,
                    "use-black": False,
                    "use-autoflake": False,
                },
            },
            "record": {"module": {"qualified": "test"}, "properties": props},
        },
    )


@pytest.fixture
def fulltext_builder():
    return ModelBuilder(
        output_builders=[InvenioRecordMarshmallowBuilder],
        outputs=[PythonOutput],
    )


def _test(fulltext_builder, string_type):
    schema = get_test_schema(a={"type": string_type})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")  # NOSONAR
    ) as f:
        data = f.read()
    assert "a = ma_fields.String()" in data


def test_fulltext(fulltext_builder):
    _test(fulltext_builder, "fulltext")


def test_fulltext_min_length(fulltext_builder):
    schema = get_test_schema(a={"type": "fulltext", "minLength": 10})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")  # NOSONAR
    ) as f:
        data = f.read()
    assert strip_whitespaces(
        "a = ma_fields.String(validate=[ma.validate.Length(min=10)])"
    ) in strip_whitespaces(data)


def test_fulltext_max_length(fulltext_builder):
    schema = get_test_schema(a={"type": "fulltext", "maxLength": 10})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")  # NOSONAR
    ) as f:
        data = f.read()
    assert strip_whitespaces(
        "a = ma_fields.String(validate=[ma.validate.Length(max=10)])"
    ) in strip_whitespaces(data)


def test_fulltext_length(fulltext_builder):
    schema = get_test_schema(a={"type": "fulltext", "maxLength": 10, "minLength": 5})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")  # NOSONAR
    ) as f:
        data = f.read()
    assert strip_whitespaces(
        "a = ma_fields.String(validate=[ma.validate.Length(min=5, max=10)])"
    ) in strip_whitespaces(data)


def test_keyword(fulltext_builder):
    _test(fulltext_builder, "keyword")


def test_fulltext_keyword(fulltext_builder):
    _test(fulltext_builder, "fulltext+keyword")


def test_integer(fulltext_builder):
    schema = get_test_schema(a={"type": "integer", "minimum": 3})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert strip_whitespaces(
        "a = ma_fields.Integer(validate=[ma.validate.Range(min=3)])"
    ) in strip_whitespaces(data)


def test_integer_min_max(fulltext_builder):
    schema = get_test_schema(a={"type": "integer", "minimum": 3, "maximum": 5})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert strip_whitespaces(
        "a = ma_fields.Integer(validate=[ma.validate.Range(min=3, max=5)])"
    ) in strip_whitespaces(data)


def test_integer_min_max_exclusive(fulltext_builder):
    schema = get_test_schema(
        a={"type": "integer", "exclusiveMinimum": 3, "exclusiveMaximum": 5}
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert strip_whitespaces(
        "a = ma_fields.Integer(validate=[ma.validate.Range(min=3, min_inclusive=False, max=5, max_inclusive=False)])"
    ) in strip_whitespaces(data)


def test_simple_array(fulltext_builder):
    schema = get_test_schema(a={"type": "array", "items": {"type": "keyword"}})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert "a = ma_fields.List(ma_fields.String())" in data


def test_simple_array_with_min_items(fulltext_builder):
    schema = get_test_schema(
        a={"type": "array", "items": {"type": "keyword"}, "minItems": 1}
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert strip_whitespaces(
        "a = ma_fields.List(ma_fields.String(), validate=[ma.validate.Length(min=1)])"
    ) in strip_whitespaces(data)


def test_array_of_objects(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "array",
            "items": {"type": "object", "properties": {"b": {"type": "integer"}}},
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class TestSchema(Schema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.List(ma_fields.Nested(lambda: AItemSchema()))

class AItemSchema(Schema):
    class Meta:
        unknown = ma.RAISE
    b = ma_fields.Integer()
"""
        )
        in strip_whitespaces(data)
    )


def test_strict_object(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            "properties": {"b": {"type": "integer"}},
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
 class ASchema(Schema):
    class Meta:
        unknown= ma.RAISE
    b= ma_fields.Integer()
"""
        )
        in strip_whitespaces(data)
    )


def test_permissive_object(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            "marshmallow": {"unknown": "INCLUDE"},
            "properties": {"b": {"type": "integer"}},
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
 class ASchema(Schema):
    class Meta:
        unknown= ma.INCLUDE
    b= ma_fields.Integer()
"""
        )
        in strip_whitespaces(data)
    )


def test_excluding_object(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            "marshmallow": {"unknown": "EXCLUDE"},
            "properties": {"b": {"type": "integer"}},
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
 class ASchema(Schema):
    class Meta:
        unknown= ma.EXCLUDE
    b= ma_fields.Integer()
"""
        )
        in strip_whitespaces(data)
    )


def test_generate_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"class": "B", "generate": True},
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.Nested(lambda: BSchema())


class BSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    b = ma_fields.String()        
        """
        )
        in strip_whitespaces(data)
    )


def test_generate_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "class": "test.services.schema2.B",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
import marshmallow as ma
from marshmallow import fields as ma_fields
from test.services.schema2 import BSchema
from marshmallow import Schema

class TestSchema(Schema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Nested(lambda: BSchema())        
        """
        )
        in strip_whitespaces(data)
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "schema2.py")  # NOSONAR
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
class BSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    b = ma_fields.String()       
        """
        )
        in strip_whitespaces(data)
    )


def test_use_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"class": "B", "generate": False},
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
        print(data)
    assert (
        strip_whitespaces(
            """
class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.Nested(lambda: B())"""
        )
        in strip_whitespaces(data)
    )
    assert strip_whitespaces("class B") not in strip_whitespaces(data)


def test_use_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {"class": "c.B", "generate": False},
            "properties": {
                "b": {
                    "type": "keyword",
                }
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert strip_whitespaces("from c import B") in strip_whitespaces(data)
    assert (
        strip_whitespaces(
            """
class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.Nested(lambda: B())"""
        )
        in strip_whitespaces(data)
    )


def test_generate_nested_schema_array(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "array",
            "items": {
                "type": "object",
                OAREPO_MARSHMALLOW: {"class": "B", "generate": True},
                "properties": {
                    "b": {
                        "type": "keyword",
                    }
                },
            },
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.List(ma_fields.Nested(lambda: BSchema()))


class BSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    b = ma_fields.String()
        """
        )
        in strip_whitespaces(data)
    )


def test_extend_existing(fulltext_builder):
    "Test that if there is a marshmallow file present on the filesystem it gets extended"
    schema = get_test_schema(a={"type": "keyword"}, b={"type": "keyword"})
    fulltext_builder.filesystem = InMemoryFileSystem()

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py"), "w"
    ) as f:
        f.write(
            '''
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
import marshmallow as ma
import marshmallow.validate as ma_valid
class TestSchema(Schema):
    """TestSchema schema."""
    a = ma_fields.String()'''
        )

    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )
    data = fulltext_builder.filesystem.read(
        os.path.join("test", "services", "records", "schema.py")
    )
    assert "b = ma_fields.String()" in data


def test_generate_nested_schema_relative_same_package(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "class": "..schema2.B",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
import marshmallow as ma
from marshmallow import fields as ma_fields
from test.services.records.schema2 import BSchema
from marshmallow import Schema

class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.Nested(lambda: BSchema())        
        """
        )
        in strip_whitespaces(data)
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema2.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class BSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    b = ma_fields.String()        
        """
        )
        in strip_whitespaces(data)
    )


def test_generate_nested_schema_relative_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "class": ".B",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.Nested(lambda: BSchema())


class BSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    b = ma_fields.String()
            """
        )
        in strip_whitespaces(data)
    )


def test_generate_nested_schema_relative_upper(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            OAREPO_MARSHMALLOW: {
                "class": "...schema2.B",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
import marshmallow as ma
from marshmallow import fields as ma_fields
from test.services.schema2 import BSchema
from marshmallow import Schema
class TestSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    a = ma_fields.Nested(lambda: BSchema())
        """
        )
        in strip_whitespaces(data)
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "schema2.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class BSchema(Schema):

    class Meta:
        unknown = ma.RAISE

    b = ma_fields.String()
        """
        )
        in strip_whitespaces(data)
    )
