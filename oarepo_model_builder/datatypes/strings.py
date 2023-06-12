import re

from marshmallow import fields
from marshmallow.exceptions import ValidationError

from .datatypes import DataType


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
    ui = {
        "marshmallow": {
            "field-class": "ma.fields.String",
        }
    }
    marshmallow = {
        "field-class": "ma.fields.String",
    }
    json_schema = {"type": "string"}

    class ModelSchema(DataType.ModelSchema):
        minLength = fields.Integer(required=False)
        maxLength = fields.Integer(required=False)
        regex = fields.String(required=False, validate=validate_regex)


class FulltextDataType(StringDataType):
    model_type = "fulltext"
    mapping = {"type": "text"}


class KeywordDataType(StringDataType):
    model_type = "keyword"
    mapping = {"type": "keyword"}
    facets = {
        "facet-class": "TermsFacet",
        "imports": [
            {"import": "invenio_records_resources.services.records.facets.TermsFacet"}
        ],
    }


class UUIDDataType(StringDataType):
    model_type = "uuid"
    mapping = {"type": "keyword"}


class FulltextKeywordDataType(StringDataType):
    model_type = "fulltext+keyword"
    mapping = {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
    facets = {
        "facet-class": "TermsFacet",
        "keyword": True,
        "path": "keyword",
        "imports": [
            {"import": "invenio_records_resources.services.records.facets.TermsFacet"}
        ],
    }


class URLDataType(StringDataType):
    model_type = "url"
    mapping = {"type": "keyword"}
    facets = {
        "facet-class": "TermsFacet",
        "imports": [
            {"import": "invenio_records_resources.services.records.facets.TermsFacet"}
        ],
    }
