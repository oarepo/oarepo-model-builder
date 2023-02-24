from marshmallow import fields

from ..utils.facet_helpers import searchable
from .datatypes import DataType


class NumberDataType(DataType):
    def marshmallow_validators(self):
        validators = []
        ranges = {}
        for param, schema in (
            ("min", "minimumExclusive"),
            ("max", "maximumExclusive"),
            ("min_inclusive", "minimum"),
            ("max_inclusive", "maximum"),
        ):
            if schema in self.definition:
                ranges[param] = self.definition[schema]

        if ranges:
            params = ", ".join(f"{k}={v}" for k, v in ranges.items())
            validators.append(f"ma_validate.Range({params})")

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


class IntegerDataType(NumberDataType):
    marshmallow_field = "ma_fields.Integer"
    schema_type = "integer"
    model_type = "integer"

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Integer(required=False)
        exclusiveMinimum = fields.Integer(required=False)
        maximum = fields.Integer(required=False)
        exclusiveMaximum = fields.Integer(required=False)
        enum = fields.List(fields.Integer(), required=False)


class FloatDataType(NumberDataType):
    marshmallow_field = "ma_fields.Float"
    schema_type = "number"
    model_type = "float"

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Float(required=False)
        exclusiveMinimum = fields.Float(required=False)
        maximum = fields.Float(required=False)
        exclusiveMaximum = fields.Float(required=False)
        enum = fields.List(fields.Float(), required=False)


class DoubleDataType(NumberDataType):
    marshmallow_field = "ma_fields.Double"
    schema_type = "number"
    model_type = "double"

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Float(required=False)
        exclusiveMinimum = fields.Float(required=False)
        maximum = fields.Float(required=False)
        exclusiveMaximum = fields.Float(required=False)
        enum = fields.List(fields.Float(), required=False)


class BooleanDataType(DataType):
    marshmallow_field = "ma_fields.Boolean"
    model_type = "boolean"

    def facet(self, key, definition={}, props_num=None, create=True):
        if not searchable(definition, create):
            return False
        key = definition.get("key", key)
        field = definition.get("field", "TermsFacet(field = ")
        facet_def = {"path": key, "class": field}
        if "field" in definition:
            facet_def["defined_class"] = True
        return facet_def
