import pytest
from marshmallow.exceptions import ValidationError

from oarepo_model_builder.validation.model_validation import model_validator


def test_empty_model_validation():
    assert model_validator.validate({}) == {
        "version": "1.0.0",
    }
    assert model_validator.validate({"model": {}}) == {
        "model": {"type": "model", "properties": {}},
        "version": "1.0.0",
    }
    with pytest.raises(ValidationError, match="Must be equal to model"):
        model_validator.validate({"model": {"type": "blah"}})
    assert model_validator.validate({"model": {"properties": {}}}) == {
        "model": {"type": "model", "properties": {}},
        "version": "1.0.0",
    }
    assert model_validator.validate(
        {"model": {"type": "model", "properties": None}}
    ) == {"model": {"type": "model", "properties": {}}, "version": "1.0.0"}


def test_unknown_on_top_validation():
    with pytest.raises(ValidationError, match="'unexpected'.*'Unknown field.'"):
        model_validator.validate({"unexpected": True})


def test_settings_on_model():
    validated = model_validator.validate(
        {
            "model": {
                "profile-package": "test",
                "package-path": "test",
                "jsonschemas-package": "test",
                "mapping": {"file": "test"},
                "model-name": "test",
                "resource-config": {"base-url": "test"},
            }
        }
    )
    assert validated == {
        "model": {
            "type": "model",
            "profile-package": "test",
            "package-path": "test",
            "jsonschemas-package": "test",
            "mapping-file": "test",
            "collection-url": "test",
            "model-name": "test",
            "properties": {},
        },
        "version": "1.0.0",
    }


def test_inline_props_on_model():
    validated = model_validator.validate(
        {
            "model": {
                "properties": {
                    "a": "boolean",
                    "b": "integer{minimum:1}",
                    "c": "float{exclusiveMaximum: 1.0}",
                    "d": "double",
                }
            }
        }
    )
    assert validated == {
        "version": "1.0.0",
        "model": {
            "type": "model",
            "properties": {
                "a": {"type": "boolean"},
                "b": {"type": "integer", "minimum": 1},
                "c": {"type": "float", "exclusiveMaximum": 1.0},
                "d": {"type": "double"},
            },
        },
    }


def test_validate_defs():
    validation_result = model_validator.validate(
        {
            "model": {},
            "$defs": {
                "a": "boolean",
                "b": "integer{minimum:1}",
                "c": "float{exclusiveMaximum: 1.0}",
                "d": "double",
            },
        }
    )
    assert validation_result == {
        "version": "1.0.0",
        "$defs": {
            "a": "boolean",
            "b": "integer{minimum:1}",
            "c": "float{exclusiveMaximum: 1.0}",
            "d": "double",
        },
        "model": {"properties": {}, "type": "model"},
    }


def test_settings():
    validation_result = model_validator.validate(
        {"model": {}, "settings": {"python": {"use-black": True, "use-isort": True}}}
    )
    assert validation_result == {
        "version": "1.0.0",
        "settings": {"python": {"use-black": True, "use-isort": True}},
        "model": {"properties": {}, "type": "model"},
    }
