from pathlib import Path

from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput

try:
    import json5
except ImportError:
    import json as json5


def test_create_simple_schema():
    class FakeBuilder:
        filesystem = InMemoryFileSystem()

    output = JSONSchemaOutput(FakeBuilder(), Path("blah.json"))
    output.begin()
    output.enter("properties", {})
    output.enter("a", {})
    output.primitive("type", "string")
    output.leave()
    output.leave()
    output.finish()

    data = json5.load(FakeBuilder.filesystem.open("blah.json"))

    assert data == {"properties": {"a": {"type": "string"}}}
