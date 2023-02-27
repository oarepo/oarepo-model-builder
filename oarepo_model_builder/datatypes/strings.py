import re
from typing import List

from marshmallow import fields
from marshmallow.exceptions import ValidationError

from ..utils.facet_helpers import searchable
from .datatypes import DataType, Import


def validate_regex(value):
    if not value:
        return
    try:
        re.compile(value)
    except Exception as e:
        raise ValidationError(
            f"Regex '{value}' is not valid. Reported error: '{str(e)}'"
        )


class StringDataType(DataType):
    schema_type = "string"
    marshmallow_field = "ma_fields.String"

    class ModelSchema(DataType.ModelSchema):
        minLength = fields.Integer(required=False)
        maxLength = fields.Integer(required=False)
        regex = fields.String(required=False, validate=validate_regex)
        enum = fields.List(fields.String(), required=False)

    def marshmallow_validators(self):
        validators = []
        ranges = {}
        for param, schema in (
            ("min", "minLength"),
            ("max", "maxLength"),
        ):
            if schema in self.definition:
                ranges[param] = self.definition[schema]

        if ranges:
            params = ", ".join(f"{k}={v}" for k, v in ranges.items())
            validators.append(f"ma_validate.Length({params})")

        if "pattern" in self.definition:
            pattern = self.definition["pattern"]
            pattern = pattern.replace("\\", "\\\\")
            pattern = pattern.replace('"', '\\"')
            validators.append(f'ma_validate.Regexp("{pattern}")')

        return validators

    def facet(self, key, definition={}, props_num=None, create=True):
        if not searchable(definition, create):
            return False
        key = definition.get("key", key)
        field = definition.get("field", "TermsFacet(field = ")
        facet_def = {"path": key, "class": field}
        if "field" in definition:
            facet_def["defined_class"] = True
        return facet_def

    @property
    def ui_marshmallow_field(self):
        if "enum" in self.definition:
            return "oarepo_ui.marshmallow.LocalizedEnum"
        return self.marshmallow_field

    def ui_marshmallow(self, **extras):
        ret = super().ui_marshmallow(**extras)
        if "enum" in self.definition:
            gettext_prefix = (
                self.definition.get("ui", {}).get("i18n-prefix")
                or self.model.get("i18n-prefix")
                or self.model.get("package")
            )
            ret.setdefault("arguments", []).extend(
                [
                    f'value_prefix="{gettext_prefix}"',
                ]
            )
        return ret

    def imports(self, *extra) -> List[Import]:
        if "enum" in self.definition:
            return super().imports(
                *extra,
                Import(
                    import_path="oarepo_ui.marshmallow.LocalizedEnum",
                    alias=None,
                ),
            )
        else:
            return super().imports(*extra)


class FulltextDataType(StringDataType):
    mapping_type = "text"
    model_type = "fulltext"

    def facet(self, key, definition=None, props_num=None, create=True):
        return False


class KeywordDataType(StringDataType):
    mapping_type = "keyword"
    model_type = "keyword"


class FulltextKeywordDataType(StringDataType):
    mapping_type = "text"
    model_type = "fulltext+keyword"

    def mapping(self):
        ret = super().mapping()
        mapping_el = ret.setdefault("mapping", {})
        mapping_el.setdefault("fields", {}).setdefault("keyword", {"type": "keyword"})
        return ret

    def facet(self, key, definition={}, props_num=None, create=True):
        if not searchable(definition, create):
            return False
        key = definition.get("key", key + "_keyword")
        field = definition.get("field", "TermsFacet(field = ")
        facet_def = {"path": key, "class": field}
        if "field" in definition:
            facet_def["defined_class"] = True
        return facet_def
