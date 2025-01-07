import json
import os

import yaml

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

from .utils import strip_whitespaces


def test_array_shortcuts():
    schema = load_model(
        "test.yaml",  # NOSONAR
        model_content={
            "record": {
                "use": "invenio",
                "properties": {"a[]": {"type": "keyword", "^required": True}},
                "module": {"qualified": "test"},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ).read()
    assert (
        strip_whitespaces(
            """
class TestSchema(BaseRecordSchema):

    class Meta:
        unknown = ma.RAISE


    a = ma_fields.List(ma_fields.String(), required=True)    
    """
        )
        in strip_whitespaces(data)
    )

    data = builder.filesystem.read(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    )
    data = json.loads(data)
    assert data == {'mappings': {'properties': {'$schema': {'ignore_above': 1024,
                                         'type': 'keyword'},
                             'a': {'ignore_above': 1024, 'type': 'keyword'},
                             'created': {'format': 'strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction',
                                         'type': 'date'},
                             'deletion_status': {'ignore_above': 1024,
                                                 'type': 'keyword'},
                             'id': {'ignore_above': 1024, 'type': 'keyword'},
                             'is_deleted': {'type': 'boolean'},
                             'is_published': {'type': 'boolean'},
                             'pid': {'properties': {'obj_type': {'ignore_above': 1024,
                                                                 'type': 'keyword'},
                                                    'pid_type': {'ignore_above': 1024,
                                                                 'type': 'keyword'},
                                                    'pk': {'type': 'integer'},
                                                    'status': {'ignore_above': 1024,
                                                               'type': 'keyword'}},
                                     'type': 'object'},
                             'updated': {'format': 'strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction',
                                         'type': 'date'},
                             'version_id': {'type': 'integer'},
                             'versions': {'properties': {'index': {'type': 'integer'},
                                                         'is_latest': {'type': 'boolean'},
                                                         'is_latest_draft': {'type': 'boolean'},
                                                         'latest_id': {'ignore_above': 1024,
                                                                       'type': 'keyword'},
                                                         'latest_index': {'type': 'integer'},
                                                         'next_draft_id': {'ignore_above': 1024,
                                                                           'type': 'keyword'}},
                                          'type': 'object'}}}}

    data = builder.filesystem.read(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    )
    data = json.loads(data)
    assert data == {'properties': {'$schema': {'type': 'string'},
                'a': {'items': {'type': 'string'}, 'type': 'array'},
                'created': {'format': 'date-time', 'type': 'string'},
                'deletion_status': {'type': 'string'},
                'id': {'type': 'string'},
                'is_deleted': {'type': 'boolean'},
                'is_published': {'type': 'boolean'},
                'pid': {'properties': {'obj_type': {'type': 'string'},
                                       'pid_type': {'type': 'string'},
                                       'pk': {'type': 'integer'},
                                       'status': {'type': 'string'}},
                        'type': 'object'},
                'updated': {'format': 'date-time', 'type': 'string'},
                'version_id': {'type': 'integer'},
                'versions': {'properties': {'index': {'type': 'integer'},
                                            'is_latest': {'type': 'boolean'},
                                            'is_latest_draft': {'type': 'boolean'},
                                            'latest_id': {'type': 'string'},
                                            'latest_index': {'type': 'integer'},
                                            'next_draft_id': {'type': 'string'}},
                             'type': 'object'}},
 'type': 'object'}


def test_singleline_type_shortcut():
    data = """
record:
  properties:
    metadata:
      properties:
        title: fulltext
  module:
    qualified: test
"""

    schema = load_model(
        "test.yaml",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
        autoflake=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")


def test_object_shortcut():
    data = """
record:
  properties:
    metadata{}:
      title: fulltext
  module:
    qualified: test
"""

    schema = load_model(
        "test.yaml",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
        autoflake=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")


def test_array_shortcut():
    data = """
record:
  module:
    qualified: test
  properties:
    metadata[]:
      type: fulltext
"""

    schema = load_model(
        "test.yaml",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
        autoflake=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")


def test_array_single_line_shortcut():
    data = """
record:
  module:
    qualified: test
  properties:
    metadata[]: fulltext
"""

    schema = load_model(
        "test.yaml",
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
        autoflake=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")


def test_misc_shortcuts():
    data = """
record:
  module:
    qualified: test
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
        model_content=yaml.safe_load(data),
        isort=False,
        black=False,
        autoflake=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")
