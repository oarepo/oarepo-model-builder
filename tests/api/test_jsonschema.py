import json
import os

from oarepo_model_builder.builders import JSONSchemaBuilder
from oarepo_model_builder.outputs import JsonSchemaOutput


def test_jsonschema_builder(model_config):
    builder = JSONSchemaBuilder()
    outputs = {}

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
    builder.pre({'oarepo:search': {'mapping': 'keyword'}}, model_config, ['properties'], outputs)
    assert builder.stack[-1] == {}
    builder.pre({'mapping': 'keyword'}, model_config, ['properties', 'oarepo:search'], outputs)
    assert builder.stack[-1] == builder.IGNORED_SUBTREE
    builder.pre('keyword', model_config, ['properties', 'oarepo:search', 'mapping'], outputs)
    assert builder.stack[-1] == builder.IGNORED_SUBTREE

    assert builder.stack[0] == {'properties': {}, **model_config.jsonschema}
    builder.pop()
    builder.pop()
    builder.pop()

    # 2.2) Valid jsonschema elements are pushed to stack/output data
    builder.pre({'field1': {'type': 'string'}}, model_config, ['properties'], outputs)
    builder.pre({'type': 'string'}, model_config, ['properties', 'field1'], outputs)
    builder.pre('string', model_config, ['properties', 'field1', 'type'], outputs)

    expected = {'properties': {'field1': {'type': 'string'}}}
    expected.update(model_config.jsonschema)

    assert builder.stack[0] == expected

    # 3) Test `pop` implementation
    assert len(builder.stack) == 4
    builder.pop()
    assert len(builder.stack) == 3
    assert builder.stack[0] == expected
    assert outputs['jsonschema'].data == expected


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
