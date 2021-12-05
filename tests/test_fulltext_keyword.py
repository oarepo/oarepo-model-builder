import os

import json5
import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.text_keyword import TextKeywordPreprocessor
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
from oarepo_model_builder.model_preprocessors.elasticsearch import ElasticsearchModelPreprocessor
from tests.mock_open import MockOpen


def get_model_schema(field_type):
    return ModelSchema(
        '',
        {
            'settings': {
                'package': 'test',
                'python': {
                    'use_isort': False,
                    'use_black': False
                }
            },
            'model': {
                'properties': {
                    'a': {
                        'type': field_type
                    }
                }
            }
        }
    )


@pytest.fixture
def fulltext_builder():
    return ModelBuilder(
        output_builders=[JSONSchemaBuilder, MappingBuilder],
        outputs=[JSONSchemaOutput, MappingOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor, ElasticsearchModelPreprocessor],
        property_preprocessors=[TextKeywordPreprocessor]
    )


def test_fulltext(fulltext_builder):
    schema = get_model_schema('fulltext')
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    data = json5.load(fulltext_builder.open(os.path.join('test', 'records', 'jsonschemas', 'test-1.0.0.json')))

    assert data == {
        'properties': {
            'a': {
                'type': 'string'
            }
        }
    }

    data = json5.load(fulltext_builder.open(os.path.join('test', 'records', 'mappings', 'v7', 'test', 'test-1.0.0.json')))

    assert data == {'mappings': {'properties': {'$schema': {'type': 'keyword'},
                                                'a': {'type': 'text'},
                                                'created': {'type': 'date'},
                                                'id': {'type': 'keyword'},
                                                'pid': {'properties': {'obj_type': {'type': 'keyword'},
                                                                       'pid_type': {'type': 'keyword'},
                                                                       'pk': {'type': 'integer'},
                                                                       'status': {'type': 'keyword'}},
                                                        'type': 'object'},
                                                'updated': {'type': 'date'},
                                                'uuid': {'type': 'keyword'}}}}


def test_keyword(fulltext_builder):
    schema = get_model_schema('keyword')
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    data = json5.load(fulltext_builder.open(os.path.join('test', 'records', 'jsonschemas', 'test-1.0.0.json')))

    assert data == {
        'properties': {
            'a': {
                'type': 'string'
            }
        }
    }

    data = json5.load(fulltext_builder.open(os.path.join('test', 'records', 'mappings', 'v7', 'test', 'test-1.0.0.json')))

    assert data == {'mappings': {'properties': {'$schema': {'type': 'keyword'},
                                                'a': {'ignore_above': 50, 'type': 'keyword'},
                                                'created': {'type': 'date'},
                                                'id': {'type': 'keyword'},
                                                'pid': {'properties': {'obj_type': {'type': 'keyword'},
                                                                       'pid_type': {'type': 'keyword'},
                                                                       'pk': {'type': 'integer'},
                                                                       'status': {'type': 'keyword'}},
                                                        'type': 'object'},
                                                'updated': {'type': 'date'},
                                                'uuid': {'type': 'keyword'}}}}


def test_fulltext_keyword(fulltext_builder):
    schema = get_model_schema('fulltext-keyword')
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    data = json5.load(fulltext_builder.open(os.path.join('test', 'records', 'jsonschemas', 'test-1.0.0.json')))

    assert data == {
        'properties': {
            'a': {
                'type': 'string'
            }
        }
    }

    data = json5.load(fulltext_builder.open(os.path.join('test', 'records', 'mappings', 'v7', 'test', 'test-1.0.0.json')))

    assert data == {'mappings': {'properties': {'$schema': {'type': 'keyword'},
                                                'a': {'fields': {'keyword': {'ignore_above': 50,
                                                                             'type': 'keyword'}},
                                                      'type': 'text'},
                                                'created': {'type': 'date'},
                                                'id': {'type': 'keyword'},
                                                'pid': {'properties': {'obj_type': {'type': 'keyword'},
                                                                       'pid_type': {'type': 'keyword'},
                                                                       'pk': {'type': 'integer'},
                                                                       'status': {'type': 'keyword'}},
                                                        'type': 'object'},
                                                'updated': {'type': 'date'},
                                                'uuid': {'type': 'keyword'}}}}
