import json
import os

from oarepo_model_builder.builders import JSONSchemaBuilder
from oarepo_model_builder.outputs import JsonSchemaOutput
from oarepo_model_builder.proxies import current_model_builder
from tests.api.helpers import _process_field


def test_jsonschema_builder(model_config):
    builder = JSONSchemaBuilder()
    outputs = {}
    config = current_model_builder.model_config

    # 1) Test that begin properly initializes outputs
    builder.begin(model_config, outputs, {})
    assert len(outputs) == 1
    assert outputs['jsonschema'].path.split('/')[-3:] == [
        'jsonschemas',
        'oarepo_model_builder',
        'oarepo-model-builder-v1.0.0.json'
    ]
    assert outputs['jsonschema'].data == model_config.jsonschema
    assert len(builder.stack) == 1
    assert builder.stack == [model_config.jsonschema]

    # 2) Test `pre` implementation

    # 2.1) `oarepo:` elements and subtrees are ignored by jsonschema
    src = {
        'field1': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'string',
                    'oarepo:search': 'text'
                }
            },
            'required': ['a'],
            'oarepo:ui': {
                'label': {}
            },
            'oarepo:search':
                {'mapping': 'keyword'}
        }
    }
    res = {
        **config.jsonschema,
        'properties': {
            'field1': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'string'
                    }
                },
                'required': ['a'],
            }
        }
    }
    builder.pre(src, config, ['properties'], outputs)
    builder.pre(src, config, ['field1'], outputs)

    path_list = [['type']]
    _process_field(builder, src['field1'], path_list, config, outputs)

    path_list = [['properties'],
                 ['properties', 'a'],
                 ['properties', 'a', 'type'],
                 ['properties', 'a', 'oarepo:search']]
    _process_field(builder, src['field1'], path_list, config, outputs)

    path_list = [['required']]
    _process_field(builder, src['field1'], path_list, config, outputs)

    path_list = [['oarepo:ui']]
    _process_field(builder, src['field1'], path_list, config, outputs)

    path_list = [['oarepo:search'],
                 ['oarepo:search', 'mapping']]
    _process_field(builder, src['field1'], path_list, config, outputs)

    assert outputs['jsonschema'].data == res


def test_jsonschema_output(model_config):
    test_path = '/tmp/test.json'
    test_data = {
        'properties': {'field1': {'type': 'number'}},
        **model_config.jsonschema
    }

    jo = JsonSchemaOutput(path=test_path, data=test_data)

    # 1) Test output initialize
    assert jo.output_type == 'jsonschema'
    assert jo.path == test_path
    assert jo.data == test_data

    # 2) Test output `save`
    assert not os.path.exists(test_path)
    jo.save()
    assert os.path.exists(test_path)

    with open(test_path, mode='r') as fp:
        saved = json.load(fp)
    os.remove(test_path)
    assert saved == test_data
