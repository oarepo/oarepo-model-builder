from pathlib import Path

from oarepo_model_builder.loaders import json_loader
from oarepo_model_builder.schema import ModelSchema

DUMMY_PATH = "/tmp/path.json"  # NOSONAR checking as it is a virtual path


def test_loading_from_string():
    schema = ModelSchema(DUMMY_PATH, {})
    assert schema.schema == {"settings": {}}


def test_loading_from_empty_file():
    schema = ModelSchema(
        Path(__file__).parent.joinpath("data/empty.json"), loaders={"json": json_loader}
    )
    assert schema.schema == {"settings": {}}


def test_loading_included_resource():
    schema = ModelSchema(
        DUMMY_PATH,
        {"a": {"use": "test1"}},
        {"test1": lambda schema: {"included": "test1"}},
    )
    assert schema.schema == {
        "settings": {},
        "a": {"included": "test1"},
    }


def test_loading_included_resource_root():
    schema = ModelSchema(
        DUMMY_PATH,
        {"use": "test1"},
        {"test1": lambda schema: {"included": "test1"}},
    )
    assert schema.schema == {
        "settings": {},
        "included": "test1",
    }


def test_loading_jsonpath_resource():
    schema = ModelSchema(
        DUMMY_PATH,
        {"use": "test1#/test/a"},
        {"test1": lambda schema: {"test": {"a": {"included": "test1"}}}},
    )
    assert schema.schema == {
        "settings": {},
        "included": "test1",
    }


def test_loading_current():
    schema = ModelSchema(DUMMY_PATH, {"b": {"use": "#/a"}, "a": {"a": True}})
    assert schema.schema == {
        "settings": {},
        "b": {"a": True},
        "a": {"a": True},
    }


def test_loading_current_by_id():
    schema = ModelSchema(
        DUMMY_PATH,
        {"b": {"use": "#id"}, "a": {"$id": "id", "a": True}},
    )
    assert schema.schema == {
        "settings": {},
        "b": {"a": True},
        "a": {"$id": "id", "a": True},
    }


def test_loading_external_by_id():
    schema = ModelSchema(
        DUMMY_PATH,
        {
            "b": {"use": "aa#id"},
        },
        {"aa": lambda schema: {"a": {"$id": "id", "a": True}}},
    )
    assert schema.schema == {
        "settings": {},
        "b": {"a": True},
    }
