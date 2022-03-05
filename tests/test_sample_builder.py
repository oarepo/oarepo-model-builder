from pathlib import Path

import faker.config

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints
from oarepo_model_builder.invenio.invenio_script_sample_data import InvenioScriptSampleDataBuilder
from oarepo_model_builder.schema import ModelSchema
from tests.mock_filesystem import MockFilesystem


def test_sample_builder_string():
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "string",
                }
            }
        )
        == "a: test\n"
    )
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "string",
                }
            },
            count=2,
        )
        == "a: test\n---\na: test\n"
    )


def test_sample_builder_integer():
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "integer",
                }
            }
        )
        == "a: 1\n"
    )


def test_sample_builder_float():
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "number",
                }
            }
        )
        == "a: 1.2\n"
    )


def test_sample_builder_date():
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "date",
                }
            }
        )
        == "a: '2022-01-02'\n"
    )


def test_sample_builder_object():
    assert (
        build_sample_data(
            {
                "obj": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "string",
                        },
                        "b": {
                            "type": "string",
                        },
                    },
                }
            }
        ).strip()
        == """
obj:
  a: test
  b: test    
    """.strip()
    )


def test_sample_builder_simple_array():
    assert (
        build_sample_data({"a": {"type": "array", "oarepo:sample": {"count": 1}, "items": {"type": "string"}}})
        == "a:\n- test\n"
    )

    # makes items unique, so expect one
    assert (
        build_sample_data({"a": {"type": "array", "oarepo:sample": {"count": 2}, "items": {"type": "string"}}})
        == "a:\n- test\n"
    )


def test_sample_builder_complex_array():
    # sampler makes items in the array unique, so expect one
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "array",
                    "oarepo:sample": {"count": 2},
                    "items": {
                        "type": "object",
                        "properties": {
                            "b": {
                                "type": "string",
                            },
                            "c": {
                                "type": "string",
                            },
                        },
                    },
                }
            }
        ).strip()
        == """
a:
- b: test
  c: test
    """.strip()
    )


def build_sample_data(model, count=1):
    faker.config.PROVIDERS.clear()
    faker.config.PROVIDERS.append("tests.faker_constant")
    builder = create_builder_from_entrypoints()
    builder.filesystem = MockFilesystem()
    builder.output_dir = Path.cwd()
    sample_builder = InvenioScriptSampleDataBuilder(builder=builder, property_preprocessors=[])
    schema = ModelSchema(
        "test.json",
        {
            "model": {"properties": model},
            "settings": {"script-import-sample-data": "test.py"},
            "oarepo:sample": {"count": count},
        },
    )
    sample_builder.build(schema)
    builder._save_outputs()
    sample_data = builder.filesystem.read("test.py")
    return sample_data
