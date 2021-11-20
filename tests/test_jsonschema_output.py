import tempfile
from pathlib import Path

from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput

try:
    import json5
except ImportError:
    import json as json5


def test_create_simple_schema():

    class FakeBuilder:
        open = open

    with tempfile.NamedTemporaryFile(suffix='.json') as tmpf:
        output = JSONSchemaOutput(FakeBuilder(), Path(tmpf.name))
        output.begin()
        output.enter('properties', {})
        output.enter('a', {})
        output.primitive('type', 'string')
        output.leave()
        output.leave()
        output.finish()
        with open(tmpf.name) as f:
            data = json5.load(f)
        assert data == {
            'properties': {
                'a': {
                    'type': 'string'
                }
            }
        }
