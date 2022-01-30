import os

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from tests.mock_filesystem import MockFilesystem


def test_no_dependencies():
    data = build()
    assert data.startswith("[tool.poetry]")


def test_runtime_dependencies():
    data = build({"runtime-dependencies": {"test": "1.0.0"}})
    assert "[tool.poetry.dependencies]" in data
    assert (
        """[tool.poetry.dependencies.test]
version = \"1.0.0\""""
        in data
    )
    assert data.index("[tool.poetry.dependencies]") < data.index("[tool.poetry.dependencies.test]")


def test_runtime_dependencies_with_extras():
    data = build({"runtime-dependencies": {"test": {"version": "1.0.0", "optional": True}}})
    assert "[tool.poetry.dependencies]" in data
    assert (
        """[tool.poetry.dependencies.test]
version = \"1.0.0\"
optional = true"""
        in data
    )
    assert data.index("[tool.poetry.dependencies]") < data.index("[tool.poetry.dependencies.test]")


def test_dev_dependencies():
    data = build({"dev-dependencies": {"test": "1.0.0"}})
    assert "[tool.poetry.dev-dependencies]" in data
    assert (
        """[tool.poetry.dev-dependencies.test]
version = \"1.0.0\""""
        in data
    )
    assert data.index("[tool.poetry.dev-dependencies]") < data.index(
        "[tool.poetry.dev-dependencies.test]"
    )


def test_dev_dependencies_with_extras():
    data = build({"dev-dependencies": {"test": {"version": "1.0.0", "optional": True}}})
    assert "[tool.poetry.dev-dependencies]" in data
    assert (
        """[tool.poetry.dev-dependencies.test]
version = \"1.0.0\"
optional = true"""
        in data
    )
    assert data.index("[tool.poetry.dev-dependencies]") < data.index(
        "[tool.poetry.dev-dependencies.test]"
    )


def build(kwargs={}):
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"model": {}, **kwargs},
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")
    data = builder.filesystem.open("pyproject.toml").read()
    return data
