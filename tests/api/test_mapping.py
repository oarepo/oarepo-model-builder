import json
import os

from oarepo_model_builder.builders import MappingBuilder
from oarepo_model_builder.outputs import MappingOutput
from oarepo_model_builder.proxies import current_model_builder
from tests.api.helpers import navigate_json


def _process_field(builder, src, path_list, config, outputs):
    for paths in path_list:
        builder.pre(navigate_json(src, *paths), config, ['properties'] + paths, outputs)
    for paths in reversed(path_list):
        builder.post(navigate_json(src, *paths), config, ['properties'] + paths, outputs)


def test_mapping_builder():
    mb = MappingBuilder()

    config = current_model_builder.model_config

    outputs = {}
    el = {}
    mb.begin(config, outputs, el)

    assert len(outputs) == 1
    assert isinstance(outputs['mapping'], MappingOutput)

    # 1) Test default mapping type without explicit mapping spec
    src = {
        'test0': {'type': 'string'},
        'testObject': {
            'type': 'object',
            'properties': {
                'field1': {'type': 'string'}
            }
        }
    }
    res = {**config.search['mapping'],
           **{
               'mappings': {
                   'properties': {
                       'test0': {'type': 'keyword'},
                       'testObject': {
                           'type': 'object',
                           'properties': {
                               'field1': {
                                   'type': 'keyword'
                               }
                           }
                       }
                   }
               }
           }}

    mb.pre(src, config, ['properties'], outputs)
    # -- process test0 field
    path_list = [['test0'], ['test0', 'type']]
    _process_field(mb, src, path_list, config, outputs)

    # -- process testObject field
    path_list = [['testObject'],
                 ['testObject', 'properties'],
                 ['testObject', 'properties', 'field1'],
                 ['testObject', 'properties', 'field1', 'type']]
    _process_field(mb, src, path_list, config, outputs)

    assert outputs['mapping'].data == res

    mb = MappingBuilder()
    mb.begin(config, outputs, el)

    # 2) Test explicit field mapping specification
    src = {
        'test1': {
            'type': 'string',
            'oarepo:search': {'mapping': 'keyword'}
        },
        'testShorthand': {
            'type': 'string',
            'oarepo:search': 'date'
        },
        'testObject': {
            'oarepo:search': {
                'mapping': {
                    'type': 'text',
                    'index': False
                }
            }
        }
    }
    res = {**config.search['mapping'],
           **{
               'mappings': {
                   'properties': {
                       'test1': {'type': 'keyword'},
                       'testShorthand': {'type': 'date'},
                       'testObject': {
                           'type': 'text',
                           'index': False
                       }
                   }
               }
           }}

    mb.pre(src, config, ['properties'], outputs)
    # -- process test1
    path_list = [['test1'], ['test1', 'oarepo:search']]
    _process_field(mb, src, path_list, config, outputs)

    # -- process testShorthand
    path_list = [['testShorthand'], ['testShorthand', 'oarepo:search']]
    _process_field(mb, src, path_list, config, outputs)

    # -- process testObject
    path_list = [['testObject'], ['testObject', 'oarepo:search']]
    _process_field(mb, src, path_list, config, outputs)

    assert outputs['mapping'].data == res

    # 3) Test items mapping
    mb = MappingBuilder()
    mb.begin(config, outputs, el)
    src = {
        'testObjItems': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'sub1': {'type': 'string'}
                }
            }
        },
        'testSimpleItems': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        'testExplicitItems': {
            'type': 'array',
            'items': {
                'type': 'string',
                'oarepo:search': 'date'
            }
        }

    }
    res = {**config.search['mapping'],
           **{
               'mappings': {
                   'properties': {
                       'testObjItems': {
                           'type': 'object',
                           'properties': {
                               'sub1': {
                                   'type': 'keyword'
                               }
                           }
                       },
                       'testSimpleItems': {
                           'type': 'keyword'
                       },
                       'testExplicitItems': {
                           'type': 'date'
                       }
                   }
               }
           }}
    mb.pre(src, config, ['properties'], outputs)

    path_list = [['testObjItems'],
                 ['testObjItems', 'items'],
                 ['testObjItems', 'items', 'properties'],
                 ['testObjItems', 'items', 'properties', 'sub1'],
                 ['testObjItems', 'items', 'properties', 'sub1', 'type']]
    _process_field(mb, src, path_list, config, outputs)

    path_list = [['testSimpleItems'],
                 ['testSimpleItems', 'items'],
                 ['testSimpleItems', 'items', 'type']]
    _process_field(mb, src, path_list, config, outputs)

    path_list = [['testExplicitItems'],
                 ['testExplicitItems', 'items'],
                 ['testExplicitItems', 'items', 'oarepo:search']]
    _process_field(mb, src, path_list, config, outputs)

    assert outputs['mapping'].data == res


def test_mapping_output():
    config = current_model_builder.model_config

    test_path = '/tmp/test.json'
    test_data = {
        'properties': {'field1': {'type': 'keyword'}},
        **config.search['mapping']
    }
    mo = MappingOutput(path='/tmp/test.json', data=test_data)

    # 1) Test output initialize
    assert mo.output_type == 'mapping'
    assert mo.path == test_path
    assert mo.data == test_data

    # 2) Test output `save`
    assert not os.path.exists(test_path)
    mo.save()
    assert os.path.exists(test_path)

    with open(test_path, mode='r') as fp:
        saved = json.load(fp)
    os.remove(test_path)
    assert saved == test_data
