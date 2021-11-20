import os
import tempfile

import json5
import pytest

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.preprocessors.text_keyword import TextKeywordPreprocessor
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.transformers.default_values import DefaultValuesTransformer
from oarepo_model_builder.transformers.elasticsearch import ElasticsearchTransformer


def get_model_schema(field_type):
    return ModelSchema(
        '',
        {
            'settings': {
                'package': 'test',
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
        transformers=[DefaultValuesTransformer, ElasticsearchTransformer],
        output_preprocessors=[TextKeywordPreprocessor]
    )


def test_fulltext(fulltext_builder):
    tmpdir = tempfile.mkdtemp()
    schema = get_model_schema('fulltext')
    fulltext_builder.build(schema, output_dir=tmpdir)

    with open(os.path.join(tmpdir, 'test', 'jsonschemas', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'string'
            }
        }
    }

    with open(os.path.join(tmpdir, 'test', 'mappings', 'v7', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'text'
            }
        }
    }


def test_keyword(fulltext_builder):
    tmpdir = tempfile.mkdtemp()
    schema = get_model_schema('keyword')
    fulltext_builder.build(schema, output_dir=tmpdir)

    with open(os.path.join(tmpdir, 'test', 'jsonschemas', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'string'
            }
        }
    }

    with open(os.path.join(tmpdir, 'test', 'mappings', 'v7', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'keyword',
                'ignore_above': 50
            }
        }
    }


def test_fulltext_keyword(fulltext_builder):
    tmpdir = tempfile.mkdtemp()
    schema = get_model_schema('fulltext-keyword')
    fulltext_builder.build(schema, output_dir=tmpdir)

    with open(os.path.join(tmpdir, 'test', 'jsonschemas', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'string'
            }
        }
    }

    with open(os.path.join(tmpdir, 'test', 'mappings', 'v7', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'text',
                'fields': {
                    'keyword': {
                        'type': 'keyword',
                        'ignore_above': 50
                    }
                }
            }
        }
    }
