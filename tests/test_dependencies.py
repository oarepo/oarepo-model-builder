import os

from oarepo_model_builder.entrypoints import (create_builder_from_entrypoints,
                                              load_model)
from oarepo_model_builder.fs import InMemoryFileSystem


def test_no_dependencies():
    data = build()
    print(data)
    assert data.startswith("[metadata]")


def test_runtime_dependencies():
    data = build({"runtime-dependencies": {"test": "1.0.0"}})
    print(data)
    assert "install_requires =" in data
    assert """test>=1.0.0""" in data
    assert data.index("install_requires") < data.index("test>=1.0.0")


def test_dev_dependencies():
    data = build({"dev-dependencies": {"test": "1.0.0"}})
    assert "[options.extras_require]" in data
    assert "devs =" in data
    assert """test>=1.0.0""" in data
    assert data.index("devs =") < data.index("test>=1.0.0")


def build(kwargs={}):
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"model": {}, **kwargs},
        isort=False,
        black=False,
    )
    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.skip_schema_validation = True
    builder.build(schema, "")
    data = builder.filesystem.open("setup.cfg").read().strip()
    return data
