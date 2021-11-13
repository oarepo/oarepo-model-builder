import os
import tempfile

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.transformers.default_values import DefaultValuesTransformer
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from tests.multilang import MultilangPreprocessor

try:
    import json5
except ImportError:
    import json as json5


def test_simple_jsonschema_builder():
    builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder],
        outputs=[JSONSchemaOutput],
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
                            'oarepo:ui': {
                                'class': 'bolder'
                            }
                        }
                    }
                }
            }
        ),
        output_dir=tmpdir
    )

    with open(os.path.join(tmpdir, 'test', 'jsonschema', 'test', 'test-1.0.0.json')) as f:
        data = json5.load(f)

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
        outputs=[JSONSchemaOutput],
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
                            'type': 'multilingual',
                            'oarepo:ui': {
                                'class': 'bolder'
                            }
                        }
                    }
                }
            }
        ),
        output_dir=tmpdir
    )

    with open(os.path.join(tmpdir, 'test', 'jsonschema', 'test', 'test-1.0.0.json')) as f:
        data = json5.load(f)

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
