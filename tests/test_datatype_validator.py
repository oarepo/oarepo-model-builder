from oarepo_model_builder.datatypes import ModelDataType, datatypes, DataType
from .multilang import UIDataTypeComponent
import pytest
import marshmallow as ma


def test_empty():
    model = {}
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", "properties": {}}


def test_bad_type():
    model = {"type": "keyword"}
    validator = ModelDataType.validator()
    with pytest.raises(ma.exceptions.ValidationError):
        validator.load(model)


def test_empty_properties():
    model = {"properties": {}}
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", "properties": {}}


def test_bad_properties():
    model = {"properties": []}
    validator = ModelDataType.validator()
    with pytest.raises(ma.exceptions.ValidationError):
        validator.load(model)


def test_simple():
    model = {"properties": {"a": {"type": "keyword"}}}
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", **model}


def test_unknown_datatype():
    model = {"properties": {"a": {"type": "__unknown__"}}}
    validator = ModelDataType.validator()
    with pytest.raises(ma.exceptions.ValidationError):
        validator.load(model)


def test_object():
    model = {
        "properties": {
            "a": {"type": "object", "properties": {"prop": {"type": "keyword"}}}
        }
    }
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", **model}


def test_nested():
    model = {
        "properties": {
            "a": {"type": "nested", "properties": {"prop": {"type": "keyword"}}}
        }
    }
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", **model}


def test_array():
    model = {"properties": {"a": {"type": "array", "items": {"type": "keyword"}}}}
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", **model}


def test_array_of_objects():
    model = {
        "properties": {
            "a": {
                "type": "array",
                "items": {
                    "type": "nested",
                    "properties": {"prop": {"type": "keyword"}},
                },
            }
        }
    }
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", **model}


def test_ui():
    datatypes.components.append(UIDataTypeComponent())
    assert UIDataTypeComponent.ModelSchema in datatypes.get_class_components(
        DataType, "ModelSchema"
    )
    model = {"properties": {"a": {"type": "keyword", "ui": {"test": "blah"}}}}
    validator = ModelDataType.validator()
    assert validator.load(model) == {"type": "model", **model}


def test_clear_cache():
    list(datatypes.components)
    datatypes.components.append(UIDataTypeComponent())
    datatypes.call_class_components(DataType, "test")
    datatypes._clear_caches()
    assert UIDataTypeComponent not in [type(x) for x in datatypes.components]
