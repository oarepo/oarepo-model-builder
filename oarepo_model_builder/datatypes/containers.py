from .datatypes import DataType


class ObjectDataType(DataType):
    schema_type = "object"
    mapping_type = "object"
    marshmallow_field = "ma_fields.Nested"
    model_type = "object"


class NestedDataType(DataType):
    schema_type = "object"
    mapping_type = "nested"
    marshmallow_field = "ma_fields.Nested"
    model_type = "nested"


class FlattenDataType(DataType):
    schema_type = "object"
    mapping_type = "flatten"
    marshmallow_field = "ma_fields.Raw"
    model_type = "flatten"


class ArrayDataType(DataType):
    schema_type = "array"
    mapping_type = None
    marshmallow_field = "ma_fields.List"
    model_type = "array"
