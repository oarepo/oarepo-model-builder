import json
import os
import re
from pathlib import Path

from oarepo_model_builder.entrypoints import load_model, create_builder_from_entrypoints
from tests.mock_filesystem import MockFilesystem


def test_include_invenio():
    schema = load_model(
        'test.yaml', 'test',
        model_content={
            'model': {
                'oarepo:use': 'invenio',
                'properties': {
                    'a': {
                        'type': 'string'
                    }
                }
            }
        }, isort=False, black=False)

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, '')

    data = builder.filesystem.open(os.path.join('test', 'services', 'schema.py')).read()

    assert re.sub(r'\s', '', data) == re.sub(r'\s', '', """
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid

class TestSchema(ma.Schema, ):
    \"""TestSchema schema.\"""
    
    a = ma_fields.String()
    
    id = ma_fields.String()
    
    created = ma_fields.Date()
    
    updated = ma_fields.Date()
    
    _schema = ma_fields.String(data_key='$schema')
    
    uuid = ma_fields.String()    
    """)

    data = builder.filesystem.read(os.path.join('test', 'records', 'mappings', 'v7', 'test', 'test-1.0.0.json'))
    data = json.loads(data)
    assert data == {
        'mappings': {
            'properties': {
                '$schema': {'ignore_above': 50, 'type': 'keyword'},
                'a': {'type': 'string'},
                'created': {'type': 'date'},
                'id': {'ignore_above': 50, 'type': 'keyword'},
                'updated': {'type': 'date'},
                'uuid': {'ignore_above': 50, 'type': 'keyword'}
            },
        }
    }


def test_generate_multiple_times():
    schema = load_model(
        'test.yaml', 'test',
        model_content={
            'model': {
                'oarepo:use': 'invenio',
                'properties': {
                    'a': {
                        'type': 'string'
                    }
                }
            }
        }, isort=False, black=False)

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, '')
    snapshot_1 = filesystem.snapshot()

    builder.build(schema, '')
    snapshot_2 = filesystem.snapshot()

    assert snapshot_1 == snapshot_2


def test_incremental_builder():
    schema = load_model(
        'test.yaml', 'test',
        model_content={
            'model': {
                'properties': {
                    'a': {
                        'type': 'string'
                    }
                }
            }
        }, isort=False, black=False)

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, '')

    schema = load_model(
        'test.yaml', 'test',
        model_content={
            'model': {
                'oarepo:use': 'invenio',
                'properties': {
                    'a': {
                        'type': 'string'
                    }
                }
            }
        }, isort=False, black=False)

    builder.build(schema, '')
    snapshot_1 = filesystem.snapshot()

    schema = load_model(
        'test.yaml', 'test',
        model_content={
            'model': {
                'oarepo:use': 'invenio',
                'properties': {
                    'a': {
                        'type': 'string'
                    }
                }
            }
        }, isort=False, black=False)
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, '')
    snapshot_2 = filesystem.snapshot()

    assert set(snapshot_1.keys()) == set(snapshot_2.keys())

    for k, iteration_result in snapshot_1.items():
        expected_result = snapshot_2[k]

        assert iteration_result == expected_result
