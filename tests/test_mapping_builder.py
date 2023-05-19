import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.outputs.mapping import MappingOutput
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema

try:
    import json5
except ImportError:
    import json as json5


def test_simple_mapping_builder():
    model = {"properties": {"a": {"type": "keyword"}}}
    data = build_model(model)

    assert data == {"mappings": {"properties": {"a": {"type": "keyword"}}}}


def test_simple_mapping_text_builder():
    model = {"properties": {"a": {"type": "keyword", "mapping": {"type": "text"}}}}
    data = build_model(model)

    assert data == {"mappings": {"properties": {"a": {"type": "text"}}}}


def test_array_mapping_builder():
    model = {
        "properties": {
            "a": {
                "type": "array",
                "items": {"type": "keyword", "mapping": {"type": "text"}},
            }
        }
    }
    data = build_model(model)

    assert data == {"mappings": {"properties": {"a": {"type": "text"}}}}


def build_model(model):
    builder = ModelBuilder(
        output_builders=[MappingBuilder],
        outputs=[MappingOutput, PythonOutput],
        filesystem=InMemoryFileSystem(),
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {
                        "use-isort": False,
                        "use-black": False,
                        "use-autoflake": False,
                    },
                    "opensearch": {"version": "os-v2"},
                },
                "record": {"module": {"qualified": "test"}, **model},
            },
        ),
        profile="record",
        model_path=["record"],
        output_dir="",
    )
    data = json5.load(
        builder.filesystem.open(
            os.path.join(
                "test", "records", "mappings", "os-v2", "test", "test-1.0.0.json"
            )
        )
    )
    return data


def test_no_index():
    model = {"properties": {"a": {"type": "keyword", "facets": {"searchable": False}}}}
    data = build_model(model)

    assert data == {
        "mappings": {"properties": {"a": {"type": "keyword", "enabled": False}}}
    }


def test_no_index_on_model():
    model = {"properties": {"a": {"type": "keyword"}}, "searchable": False}
    data = build_model(model)

    assert data == {
        "mappings": {"properties": {"a": {"type": "keyword", "enabled": False}}}
    }


def test_override_no_index_on_model():
    model = {
        "properties": {"a": {"type": "keyword", "facets": {"searchable": True}}},
        "searchable": False,
    }
    data = build_model(model)

    assert data == {"mappings": {"properties": {"a": {"type": "keyword"}}}}


def test_override_no_index_on_model():
    model = {
        "properties": {"a": {"type": "keyword", "facets": {"searchable": True}}},
        "searchable": False,
    }
    data = build_model(model)

    assert data == {"mappings": {"properties": {"a": {"type": "keyword"}}}}


def test_deep_no_index():
    model = {
        "properties": {
            "a": {
                "type": "object",
                "facets": {"searchable": False},
                "properties": {"b": {"type": "keyword"}},
            }
        }
    }
    data = build_model(model)

    assert data == {
        "mappings": {
            "properties": {
                "a": {
                    "type": "object",
                    "enabled": False,
                }
            }
        }
    }


def test_deep_no_index_children():
    model = {
        "properties": {
            "a": {
                "type": "object",
                "properties": {
                    "b": {"type": "keyword", "facets": {"searchable": False}}
                },
            }
        }
    }
    data = build_model(model)

    assert data == {
        "mappings": {
            "properties": {
                "a": {
                    "type": "object",
                    "enabled": False,
                }
            }
        }
    }
