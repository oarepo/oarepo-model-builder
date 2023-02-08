from typing import List

from marshmallow import fields

from .datatypes import DataType, Import


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


class IntegerDataType(NumberDataType):
    marshmallow_field = "ma_fields.Integer"
    schema_type = "integer"
    model_type = "integer"

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Integer(required=False)
        exclusiveMinimum = fields.Integer(required=False)
        maximum = fields.Integer(required=False)
        exclusiveMaximum = fields.Integer(required=False)


class FloatDataType(NumberDataType):
    marshmallow_field = "ma_fields.Float"
    schema_type = "number"
    model_type = "float"

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Float(required=False)
        exclusiveMinimum = fields.Float(required=False)
        maximum = fields.Float(required=False)
        exclusiveMaximum = fields.Float(required=False)


class DoubleDataType(NumberDataType):
    marshmallow_field = "ma_fields.Double"
    schema_type = "number"
    model_type = "double"

    class ModelSchema(DataType.ModelSchema):
        minimum = fields.Float(required=False)
        exclusiveMinimum = fields.Float(required=False)
        maximum = fields.Float(required=False)
        exclusiveMaximum = fields.Float(required=False)


class BooleanDataType(DataType):
    marshmallow_field = "ma_fields.Boolean"
    model_type = "boolean"
