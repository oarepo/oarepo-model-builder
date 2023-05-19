import pytest
from marshmallow.exceptions import ValidationError

from oarepo_model_builder.validation.model_validation import model_validator


def test_empty_model_validation():
    assert model_validator.validate({}) == {
        "version": "1.0.0",
        "settings": {"schema-server": "local://"},  # NOSONAR
    }
    assert model_validator.validate({"record": {}}) == {
        "record": {"type": "model", "properties": {}, "searchable": True},
        "settings": {"schema-server": "local://"},
        "version": "1.0.0",
    }
    with pytest.raises(ValidationError, match="Must be equal to model"):
        model_validator.validate({"record": {"type": "blah"}})
    assert model_validator.validate({"record": {"properties": {}}}) == {
        "record": {"type": "model", "properties": {}, "searchable": True},
        "settings": {"schema-server": "local://"},
        "version": "1.0.0",
    }
    assert model_validator.validate(
        {"record": {"type": "model", "properties": None}}
    ) == {
        "record": {"type": "model", "properties": {}, "searchable": True},
        "settings": {"schema-server": "local://"},
        "version": "1.0.0",
    }


def test_unknown_on_top_validation():
    with pytest.raises(ValidationError, match="'unexpected'.*'Unknown field.'"):
        model_validator.validate({"unexpected": True})


def test_settings_on_model():
    validated = model_validator.validate(
        {
            "record": {
                "module": {"qualified": "test"},
                "json-schema-settings": {"file": "test"},
                "mapping-settings": {"file": "test"},
                "model-name": "test",
                "resource-config": {"base-url": "test"},
            }
        }
    )
    assert validated == {
        "record": {
            "json-schema-settings": {"file": "test"},
            "mapping-settings": {"file": "test"},
            "model-name": "test",
            "module": {"qualified": "test"},
            "properties": {},
            "resource-config": {"base-url": "test"},
            "type": "model",
            "searchable": True,
        },
        "settings": {"schema-server": "local://"},
        "version": "1.0.0",
    }


def test_inline_props_on_model():
    validated = model_validator.validate(
        {
            "record": {
                "properties": {
                    "a": "boolean",
                    "b": "integer{minimum:1}",              # NOSONAR
                    "c": "float{exclusiveMaximum: 1.0}",    # NOSONAR
                    "d": "double",
                }
            }
        }
    )
    assert validated == {
        "version": "1.0.0",
        "record": {
            "type": "model",
            "properties": {
                "a": {"type": "boolean"},
                "b": {"type": "integer", "minimum": 1},
                "c": {"type": "float", "exclusiveMaximum": 1.0},
                "d": {"type": "double"},
            },
            "searchable": True,
        },
        "settings": {"schema-server": "local://"},
    }


def test_validate_defs():
    validation_result = model_validator.validate(
        {
            "record": {},
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
        "record": {"properties": {}, "type": "model", "searchable": True},
        "settings": {"schema-server": "local://"},
    }


def test_settings():
    validation_result = model_validator.validate(
        {"record": {}, "settings": {"python": {"use-black": True, "use-isort": True}}}
    )
    assert validation_result == {
        "version": "1.0.0",
        "settings": {
            "python": {"use-black": True, "use-isort": True, "use-autoflake": True},
            "schema-server": "local://",
        },
        "record": {"properties": {}, "type": "model", "searchable": True},
    }
