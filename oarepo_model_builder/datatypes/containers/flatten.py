from ..datatypes import DataType


class FlatObjectDataType(DataType):
    model_type = "flat_object"

    ui = {
        "marshmallow": {
            "field-class": "ma.fields.Dict",
        }
    }
    marshmallow = {
        "field-class": "ma.fields.Dict",
    }
    json_schema = {"type": "object"}
    mapping = {"type": "flat_object"}
