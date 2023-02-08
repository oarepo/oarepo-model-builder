import sys

import pytest
from marshmallow.exceptions import ValidationError

from oarepo_model_builder.validation.model_validation import model_validator


def test_empty_model_validation():
    model_validator.validate({})
    model_validator.validate({"model": {}})
    model_validator.validate({"model": {"type": "object"}})
    with pytest.raises(ValidationError, match="Bad value.*'object' expected"):
        model_validator.validate({"model": {"type": "blah"}})
    model_validator.validate({"model": {"type": "object", "properties": {}}})
    model_validator.validate({"model": {"type": "object", "properties": None}})


def test_unknown_on_top_validation():
    with pytest.raises(ValidationError, match="'unexpected'.*'Unknown field.'"):
        model_validator.validate({"unexpected": True})


def test_settings_on_model():
    model_validator.validate(
        {
            "model": {
                "profile-package": "test",
                "package-path": "test",
                "jsonschemas-package": "test",
                "mapping-file": "test",
                "collection-url": "test",
                "model-name": "test",
            }
        }
    )


def test_inline_props_on_model():
    assert model_validator.validate(
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
    ) == {
        "version": "1.0.0",
        "model": {
            "type": "object",
            "properties": {
                "a": {"type": "boolean"},
                "b": {"type": "integer", "minimum": 1},
                "c": {"type": "float", "exclusiveMaximum": 1.0},
                "d": {"type": "double"},
            },
        },
    }
