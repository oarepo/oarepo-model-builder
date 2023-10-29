from ..datatypes import DataType


class FlatObjectDataType(DataType):
    model_type = "flat_object"

    ui = {
        "marshmallow": {
            "field-class": "marshmallow.fields{ma_fields.Dict}",
        }
    }
    marshmallow = {
        "field-class": "marshmallow.fields{ma_fields.Dict}",
    }
    json_schema = {"type": "object"}
    mapping = {"type": "flat_object"}
