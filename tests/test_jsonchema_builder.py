import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from tests.mock_open import MockOpen
from tests.multilang import MultilangPreprocessor

try:
    import json5
except ImportError:
    import json as json5


def test_simple_jsonschema_builder():
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        open=MockOpen()
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
                    }
                },
                'model': {
                    'properties': {
                        'a': {
                            'type': 'string',
                            'oarepo:ui': {
                                'class': 'bolder'
                            }
                        }
                    }
                }
            }
        ),
        output_dir=''
    )

    data = json5.load(builder.open(os.path.join('test', 'jsonschemas', 'test-1.0.0.json')))

    assert data == {
        'properties': {
            'a': {
                'type': 'string'
            }
        }
    }


def test_jsonschema_preprocessor():
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor],
        output_preprocessors=[MultilangPreprocessor],
        open=MockOpen()
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
                    }
                },
                'model': {
                    'properties': {
                        'a': {
                            'type': 'multilingual',
                            'oarepo:ui': {
                                'class': 'bolder'
                            }
                        }
                    }
                }
            }
        ),
        output_dir=''
    )

    data = json5.load(builder.open(os.path.join('test', 'jsonschemas', 'test-1.0.0.json')))

    assert data == {
        'properties': {
            'a': {
                'type': 'object',
                'properties': {
                    'lang': {
                        'type': 'string'
                    },
                    'value': {
                        'type': 'string'
                    }
                }
            }
        }
    }
