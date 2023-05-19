import os

import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_record_resource_config import (
    InvenioRecordResourceConfigBuilder,
)
from oarepo_model_builder.invenio.invenio_record_ui_marshmallow import (
    InvenioRecordUIMarshmallowBuilder,
)
from oarepo_model_builder.invenio.invenio_record_ui_serializer import (
    InvenioRecordUISerializerBuilder,
)
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema

from .utils import strip_whitespaces


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
        output_builders=[
            InvenioRecordUIMarshmallowBuilder,
            InvenioRecordUISerializerBuilder,
            InvenioRecordResourceConfigBuilder,
        ],
        outputs=[PythonOutput],
    )


def _test(fulltext_builder, string_type):
    schema = get_test_schema(a={"type": string_type})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """ 
class TestUISchema(InvenioUISchema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.List(ma_fields.Nested(lambda: AItemUISchema()))


class AItemUISchema(ma.Schema):

    class Meta:
        unknown = ma.RAISE


    b = ma_fields.Integer() """
        )
        in strip_whitespaces(data)
    )


def test_generate_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            "marshmallow": {"class": "B", "generate": True},
            "ui": {"marshmallow": {"class": "BUISchema", "generate": True}},
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
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class TestUISchema(InvenioUISchema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.Nested(lambda: BUISchema())


class BUISchema(ma.Schema):

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
            "marshmallow": {
                "class": "test.services.schema2.B",
                "generate": True,
            },
            "ui": {
                "marshmallow": {
                    "class": "test.services.schema2.BUISchema",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
from test.services.schema2 import BUISchema
class TestUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Nested(lambda: BUISchema())
    """
        )
        in strip_whitespaces(data)
    )


def test_use_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            "marshmallow": {"class": "B", "generate": False},
            "ui": {"marshmallow": {"class": "BUISchema", "generate": False}},
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
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
class TestUISchema(InvenioUISchema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.Nested(lambda: BUISchema())
"""
        )
        in strip_whitespaces(data)
    )

    assert strip_whitespaces("class BUISchema") not in strip_whitespaces(data)


def test_use_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            "marshmallow": {"class": "c.B", "generate": False},
            "ui": {"marshmallow": {"class": "c.BUISchema", "generate": False}},
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
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
from c import BUISchema
from oarepo_runtime.ui.marshmallow import InvenioUISchema
class TestUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Nested(lambda: BUISchema())
"""
        )
        in strip_whitespaces(data)
    )


def test_generate_nested_schema_array(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "array",
            "items": {
                "type": "object",
                "marshmallow": {"class": "B", "generate": True},
                "ui": {"marshmallow": {"class": "BUISchema", "generate": True}},
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
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class TestUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.List(ma_fields.Nested(lambda: BUISchema()))


class BUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE
    b = ma_fields.String()
"""
        )
        in strip_whitespaces(data)
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

    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )
    data = fulltext_builder.filesystem.read(
        os.path.join("test", "services", "records", "ui_schema.py")
    )
    assert "b = ma_fields.String()" in data


def test_generate_nested_schema_relative_same_package(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "object",
            "marshmallow": {
                "class": ".schema2.B",
                "generate": True,
            },
            "ui": {
                "marshmallow": {
                    "class": "..ui_schema2.BUISchema",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class TestUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Nested(lambda: BUISchema())
"""
        )
        in strip_whitespaces(data)
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema2.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            """
class BUISchema(ma.Schema):
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
            "marshmallow": {
                "class": ".B",
                "generate": True,
            },
            "ui": {
                "marshmallow": {
                    "class": ".BUISchema",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
class TestUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Nested(lambda: BUISchema())

class BUISchema(ma.Schema):
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
            "marshmallow": {
                "class": "...schema2.B",
                "generate": True,
            },
            "ui": {
                "marshmallow": {
                    "class": "..schema2.BUISchema",
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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()

    assert (
        strip_whitespaces(
            """
from test.services.records.schema2 import BUISchema
class TestUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE
    a = ma_fields.Nested(lambda: BUISchema())
"""
        )
        in strip_whitespaces(data)
    )


def test_generate_json_serializer(fulltext_builder):
    schema = get_test_schema(
        a={
            "type": "keyword",
        }
    )
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )
    with fulltext_builder.filesystem.open(
        os.path.join("test", "resources", "records", "ui.py")
    ) as f:
        data = f.read()
    assert (
        strip_whitespaces(
            '''
from flask_resources import BaseListSchema
from flask_resources import MarshmallowSerializer
from flask_resources.serializers import JSONSerializer

from test.services.records.ui_schema import TestUISchema



class TestUIJSONSerializer(MarshmallowSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=TestUISchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui"},
        )    
    '''
        )
        == strip_whitespaces(data)
    )


def test_localized_date(fulltext_builder):
    schema = get_test_schema(a={"type": "date"})
    fulltext_builder.filesystem = InMemoryFileSystem()
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

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
    fulltext_builder.build(
        schema, profile="record", model_path=["record"], output_dir=""
    )

    with fulltext_builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ) as f:
        data = f.read()
    assert "metadata = ma_fields.Nested(lambda: TestMetadataUISchema())" in data
