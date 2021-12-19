import os
import re

import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.model_preprocessors.invenio import InvenioModelPreprocessor
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.property_preprocessors.text_keyword import TextKeywordPreprocessor
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
from oarepo_model_builder.model_preprocessors.elasticsearch import ElasticsearchModelPreprocessor
from tests.mock_open import MockOpen


def get_test_schema(**props):
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
                'properties': props
            }
        }
    )


@pytest.fixture
def fulltext_builder():
    return ModelBuilder(
        output_builders=[InvenioRecordSchemaBuilder],
        outputs=[PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor, ElasticsearchModelPreprocessor, InvenioModelPreprocessor],
        property_preprocessors=[TextKeywordPreprocessor]
    )


def _test(fulltext_builder, string_type):
    schema = get_test_schema(a={
        'type': string_type
    })
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()
    print(data)
    assert 'a = ma_fields.String()' in data


def test_fulltext(fulltext_builder):
    _test(fulltext_builder, 'fulltext')


def test_keyword(fulltext_builder):
    _test(fulltext_builder, 'keyword')


def test_fulltext_keyword(fulltext_builder):
    _test(fulltext_builder, 'fulltext-keyword')


def test_simple_array(fulltext_builder):
    schema = get_test_schema(a={
        'type': 'array',
        'items': {
            'type': 'string'
        }
    })
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()
    assert 'a = ma.List(ma_fields.String())' in data


def test_generate_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(a={
        'oarepo:marshmallow': {
            'class': 'B',
            'generate': True
        },
        'properties': {
            'b': {
                'type': 'string',
            }
        }
    })
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()

    assert 'classB(ma.Schema,):"""Bschema."""b=ma_fields.String()' in re.sub(r'\s', '', data)
    assert 'classTestSchema(ma.Schema,):"""TestSchemaschema."""a=ma_fields.Nested(B())' in re.sub(r'\s', '', data)


def test_generate_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(a={
        'oarepo:marshmallow': {
            'class': 'test.services.schema2.B',
            'generate': True
        },
        'properties': {
            'b': {
                'type': 'string',
            }
        }
    })
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()
    print(data)
    assert 'classTestSchema(ma.Schema,):"""TestSchemaschema."""a=ma_fields.Nested(B())' in re.sub(r'\s', '', data)
    assert 'from test.services.schema2 import B' in data

    with fulltext_builder.open(os.path.join('test', 'services', 'schema2.py')) as f:
        data = f.read()
    assert 'classB(ma.Schema,):"""Bschema."""b=ma_fields.String()' in re.sub(r'\s', '', data)


def test_use_nested_schema_same_file(fulltext_builder):
    schema = get_test_schema(a={
        'oarepo:marshmallow': {
            'class': 'B',
            'generate': False
        },
        'properties': {
            'b': {
                'type': 'string',
            }
        }
    })
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()

    assert 'classB(ma.Schema,)' not in re.sub(r'\s', '', data)
    assert 'classTestSchema(ma.Schema,):"""TestSchemaschema."""a=ma_fields.Nested(B())' in re.sub(r'\s', '', data)


def test_use_nested_schema_different_file(fulltext_builder):
    schema = get_test_schema(a={
        'oarepo:marshmallow': {
            'class': 'c.B',
            'generate': False
        },
        'properties': {
            'b': {
                'type': 'string',
            }
        }
    })
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()
    print(data)
    assert re.sub(r'\s', '', 'from c import B') in re.sub(r'\s', '', data)
    assert 'classTestSchema(ma.Schema,):"""TestSchemaschema."""a=ma_fields.Nested(B())' in re.sub(r'\s', '', data)


def test_generate_nested_schema_array(fulltext_builder):
    schema = get_test_schema(a={
        'type': 'array',
        'items': {
            'oarepo:marshmallow': {
                'class': 'B',
                'generate': True
            },
            'properties': {
                'b': {
                    'type': 'string',
                }
            }
        }
    })
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()
    print(data)
    assert 'classB(ma.Schema,):"""Bschema."""b=ma_fields.String()' in re.sub(r'\s', '', data)
    assert 'classTestSchema(ma.Schema,):"""TestSchemaschema."""a=ma.List(ma_fields.Nested(B()))' in re.sub(r'\s', '', data)
