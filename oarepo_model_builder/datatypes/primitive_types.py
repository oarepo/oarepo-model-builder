from marshmallow import fields

from .datatypes import DataType


class NumberDataType(DataType):
    facets = {
        "facet-class": "TermsFacet",
        "imports": [
            {"import": "invenio_records_resources.services.records.facets.TermsFacet"}
        ],
    }


class IntegerDataType(NumberDataType):
    model_type = "integer"

    ui = {
        "marshmallow": {
            "field-class": "ma.fields.Integer",
        }
    }
    marshmallow = {
        "field-class": "ma.fields.Integer",
    }
    json_schema = {"type": "integer"}

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Integer(required=False)
        exclusiveMinimum = fields.Integer(required=False)
        maximum = fields.Integer(required=False)
        exclusiveMaximum = fields.Integer(required=False)
        enum = fields.List(fields.Integer(), required=False)


class FloatDataType(NumberDataType):
    model_type = "float"

    ui = {
        "marshmallow": {
            "field-class": "ma.fields.Float",  # NOSONAR
        }
    }
    marshmallow = {
        "field-class": "ma.fields.Float",
    }
    json_schema = {"type": "number"}

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Float(required=False)
        exclusiveMinimum = fields.Float(required=False)
        maximum = fields.Float(required=False)
        exclusiveMaximum = fields.Float(required=False)
        enum = fields.List(fields.Float(), required=False)


class DoubleDataType(NumberDataType):
    model_type = "double"

    ui = {
        "marshmallow": {
            "field-class": "ma.fields.Float",
        }
    }
    marshmallow = {
        "field-class": "ma.fields.Float",
    }
    json_schema = {"type": "number"}

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Float(required=False)
        exclusiveMinimum = fields.Float(required=False)
        maximum = fields.Float(required=False)
        exclusiveMaximum = fields.Float(required=False)
        enum = fields.List(fields.Float(), required=False)


class BooleanDataType(DataType):
    model_type = "boolean"

    ui = {
        "marshmallow": {
            "field-class": "ma.fields.Boolean",
        }
    }
    marshmallow = {
        "field-class": "ma.fields.Boolean",
    }
    json_schema = {"type": "boolean"}
    facets = {
        "facet-class": "TermsFacet",
        "imports": [
            {"import": "invenio_records_resources.services.records.facets.TermsFacet"}
        ],
    }
