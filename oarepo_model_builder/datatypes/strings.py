from .datatypes import DataType
from marshmallow import fields
from marshmallow.exceptions import ValidationError
import re


def validate_regex(value):
    if not value:
        return
    try:
        re.compile(value)
    except Exception as e:
        raise ValidationError(f"Regex '{value}' is not valid. Reported error: '{str(e)}'")

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


    def facet(self, key, definition={}, props_num=None):
        name = definition.get('key', key)
        field = definition.get('field', "TermsFacet(field = ")
        return {"path": name, "class": field}

class FulltextDataType(StringDataType):
    mapping_type = "text"
    model_type = "fulltext"

    def facet(self, key, definition=None, props_num=None):
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

    def facet(self, key, definition={}, props_num = None):
        key = definition.get('key', key + "_keyword")
        field = definition.get('field', "TermsFacet(field = ")
        return {"path": key, "class" : field}