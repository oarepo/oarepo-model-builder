import os
import tempfile

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.transformers.default_values import DefaultValuesTransformer
from oarepo_model_builder.builders.mapping import MappingBuilder
from tests.multilang import MultilangPreprocessor

try:
    import json5
except ImportError:
    import json as json5


def test_simple_mapping_builder():
    builder = ModelBuilder(
        output_builders=[MappingBuilder],
        outputs=[MappingOutput],
        transformers=[DefaultValuesTransformer],
    )
    tmpdir = tempfile.mkdtemp()
    builder.build(
        schema=ModelSchema(
            '',
            {
                'package': 'test',
                'model': {
                    'properties': {
                        'a': {
                            'type': 'string',
                            'oarepo:mapping': {
                                'type': 'text'
                            }
                        }
                    }
                }
            }
        ),
        output_dir=tmpdir
    )

    with open(os.path.join(tmpdir, 'test', 'mapping', 'v7', 'test', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'text'
            }
        }
    }


def test_mapping_preprocessor():
    builder = ModelBuilder(
        output_builders=[MappingBuilder],
        outputs=[MappingOutput],
        transformers=[DefaultValuesTransformer],
        output_preprocessors=[MultilangPreprocessor]
    )

    tmpdir = tempfile.mkdtemp()
    builder.build(
        schema=ModelSchema(
            '',
            {
                'package': 'test',
                'model': {
                    'properties': {
                        'a': {
                            'type': 'multilingual'
                        }
                    }
                }
            }
        ),
        output_dir=tmpdir
    )

    with open(os.path.join(tmpdir, 'test', 'mapping', 'v7', 'test', 'test-1.0.0.json')) as f:
        data = json5.load(f)

    assert data == {
        'properties': {
            'a': {
                'type': 'object',
                'properties': {
                    'lang': {
                        'type': 'keyword'
                    },
                    'value': {
                        'type': 'text'
                    }
                }
            },
            'a_cs': {
                'type': 'text'
            }
        }
    }
