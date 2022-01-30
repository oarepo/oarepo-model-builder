from pathlib import Path

from oarepo_model_builder.loaders import json_loader
from oarepo_model_builder.schema import ModelSchema


def test_loading_from_string():
    schema = ModelSchema("/tmp/path.json", {})
    assert schema.schema == {"settings": {"plugins": {}}}


def test_loading_from_empty_file():
    schema = ModelSchema(
        Path(__file__).parent.joinpath("data/empty.json"), loaders={"json": json_loader}
    )
    assert schema.schema == {"settings": {"plugins": {}}}


def test_loading_included_resource():
    schema = ModelSchema(
        "/tmp/path.json",
        {"a": {"oarepo:use": "test1"}},
        {"test1": lambda schema: {"included": "test1"}},
    )
    assert schema.schema == {
        "settings": {"plugins": {}},
        "a": {"oarepo:included-from": "test1", "included": "test1"},
    }


def test_loading_included_resource_root():
    schema = ModelSchema(
        "/tmp/path.json",
        {"oarepo:use": "test1"},
        {"test1": lambda schema: {"included": "test1"}},
    )
    assert schema.schema == {
        "settings": {"plugins": {}},
        "oarepo:included-from": "test1",
        "included": "test1",
    }


def test_loading_jsonpath_resource():
    schema = ModelSchema(
        "/tmp/path.json",
        {"oarepo:use": "test1#/test/a"},
        {"test1": lambda schema: {"test": {"a": {"included": "test1"}}}},
    )
    assert schema.schema == {
        "settings": {"plugins": {}},
        "oarepo:included-from": "test1#/test/a",
        "included": "test1",
    }


def test_loading_current():
    schema = ModelSchema(
        "/tmp/path.json", {"b": {"oarepo:use": "#/a"}, "a": {"a": True}}
    )
    assert schema.schema == {
        "settings": {"plugins": {}},
        "b": {"oarepo:included-from": "#/a", "a": True},
        "a": {"a": True},
    }


def test_loading_current_by_id():
    schema = ModelSchema(
        "/tmp/path.json", {"b": {"oarepo:use": "#id"}, "a": {"$id": "id", "a": True}}
    )
    assert schema.schema == {
        "settings": {"plugins": {}},
        "b": {"oarepo:included-from": "#id", "a": True},
        "a": {"$id": "id", "a": True},
    }


def test_loading_external_by_id():
    schema = ModelSchema(
        "/tmp/path.json",
        {
            "b": {"oarepo:use": "aa#id"},
        },
        {"aa": lambda schema: {"a": {"$id": "id", "a": True}}},
    )
    assert schema.schema == {
        "settings": {"plugins": {}},
        "b": {"oarepo:included-from": "aa#id", "a": True},
    }
