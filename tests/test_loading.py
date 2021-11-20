from pathlib import Path

from oarepo_model_builder.loaders import json_loader
from oarepo_model_builder.schema import ModelSchema


def test_loading_from_string():
    schema = ModelSchema('/tmp/path.json', {})
    assert schema.schema == {'settings': {}}


def test_loading_from_empty_file():
    schema = ModelSchema(Path(__file__).parent.joinpath('data/empty.json'), loaders={
        'json': json_loader
    })
    assert schema.schema == {'settings': {}}


def test_loading_included_resource():
    schema = ModelSchema('/tmp/path.json', {
        'a': {
            'oarepo:use': 'test1'
        }
    }, {
                             'test1': lambda schema: {
                                 'included': 'test1'
                             }
                         })
    assert schema.schema == {
        'settings': {},
        'a': {
            'included': 'test1'
        }
    }


def test_loading_included_resource_root():
    schema = ModelSchema(
        '/tmp/path.json', {
            'oarepo:use': 'test1'
        }, {
            'test1': lambda schema: {
                'included': 'test1'
            }
        })
    assert schema.schema == {
        'settings': {},
        'included': 'test1'
    }
