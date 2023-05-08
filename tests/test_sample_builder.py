import faker.config

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_script_sample_data import SampleDataBuilder
from oarepo_model_builder.outputs.yaml import YAMLOutput
from oarepo_model_builder.schema import ModelSchema


def test_sample_builder_string():
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "keyword",
                }
            }
        )
        == "a: test\n"
    )
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "keyword",
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
                    "type": "float",
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
                            "type": "keyword",
                        },
                        "b": {
                            "type": "keyword",
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
        build_sample_data(
            {
                "a": {
                    "type": "array",
                    "sample": {"count": 1},
                    "items": {"type": "keyword"},
                }
            }
        )
        == "a:\n- test\n"
    )

    # makes items unique, so expect one
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "array",
                    "sample": {"count": 2},
                    "items": {"type": "keyword"},
                }
            }
        )
        == "a:\n- test\n"
    )


def test_sample_builder_complex_array():
    # sampler makes items in the array unique, so expect one
    assert (
        build_sample_data(
            {
                "a": {
                    "type": "array",
                    "sample": {"count": 2},
                    "items": {
                        "type": "object",
                        "properties": {
                            "b": {
                                "type": "keyword",
                            },
                            "c": {
                                "type": "keyword",
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
    builder = ModelBuilder(
        output_builders=[SampleDataBuilder],
        outputs=[YAMLOutput],
        filesystem=InMemoryFileSystem(),
    )
    schema = ModelSchema(
        "test.json",
        {
            "record": {
                "sample": {"file": "test.yaml", "count": count},
                "module": {"qualified": "test"},
                "properties": {
                    **model,
                },
            },
            "settings": {},
        },
    )
    builder.build(schema, "record", ["record"], output_dir="")
    sample_data = builder.filesystem.read("test.yaml")
    return sample_data
