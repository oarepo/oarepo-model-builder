import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
from oarepo_model_builder.builders.mapping import MappingBuilder
from tests.mock_filesystem import MockFilesystem
from tests.multilang import MultilangPreprocessor

try:
    import json5
except ImportError:
    import json as json5


def test_simple_mapping_builder():
    builder = ModelBuilder(
        output_builders=[MappingBuilder],
        outputs=[MappingOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        filesystem=MockFilesystem()
    )
    builder.build(
        schema=ModelSchema(
            '',
            {
                'settings': {
                    'package': 'test',
                    'python': {
                        'use_isort': False,
                        'use_black': False
                    },
                    'elasticsearch': {
                        'version': 'v7',
                        'templates': {
                            'v7': {}
                        }
                    }
                },
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
        output_dir=''
    )

    data = json5.load(builder.filesystem.open(os.path.join('test', 'model', 'mappings', 'v7', 'test', 'test-1.0.0.json')))

    assert data == {'mappings': {'properties': {'a': {'type': 'text'}}}}


def test_mapping_preprocessor():
    builder = ModelBuilder(
        output_builders=[MappingBuilder],
        outputs=[MappingOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        property_preprocessors=[MultilangPreprocessor],
        filesystem=MockFilesystem()
    )

    builder.build(
        schema=ModelSchema(
            '',
            {
                'settings': {
                    'package': 'test',
                    'python': {
                        'use_isort': False,
                        'use_black': False
                    },
                    'elasticsearch': {
                        'version': 'v7',
                        'templates': {
                            'v7': {}
                        }
                    }
                },
                'model': {
                    'properties': {
                        'a': {
                            'type': 'multilingual'
                        }
                    }
                }
            }
        ),
        output_dir=''
    )

    data = json5.load(builder.filesystem.open(os.path.join('test', 'model', 'mappings', 'v7', 'test', 'test-1.0.0.json')))

    assert data == {
        "mappings": {
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
    }
