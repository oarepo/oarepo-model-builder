from typing import List

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


class FloatDataType(NumberDataType):
    marshmallow_field = "ma_fields.Float"
    schema_type = "number"
    model_type = "float"


class DoubleDataType(NumberDataType):
    marshmallow_field = "ma_fields.Double"
    schema_type = "number"
    model_type = "double"


class BooleanDataType(DataType):
    marshmallow_field = "ma_fields.Boolean"
    model_type = "boolean"
