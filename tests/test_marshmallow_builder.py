import os

import json5
import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.model_preprocessors.invenio import InvenioModelPreprocessor
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
        output_builders=[InvenioRecordSchemaBuilder],
        outputs=[PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor, ElasticsearchModelPreprocessor, InvenioModelPreprocessor],
        property_preprocessors=[TextKeywordPreprocessor]
    )


def _test(fulltext_builder, string_type):
    schema = get_model_schema(string_type)
    fulltext_builder.open = MockOpen()
    fulltext_builder.build(schema, output_dir='')

    with fulltext_builder.open(os.path.join('test', 'services', 'schema.py')) as f:
        data = f.read()

    assert 'a = ma_fields.String()' in data


def test_fulltext(fulltext_builder):
    _test(fulltext_builder, 'fulltext')


def test_keyword(fulltext_builder):
    _test(fulltext_builder, 'keyword')


def test_fulltext_keyword(fulltext_builder):
    _test(fulltext_builder, 'fulltext-keyword')
