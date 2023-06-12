from ..datatypes import DataType


class FlattenDataType(DataType):
    model_type = "flattened"

    ui = {
        "marshmallow": {
            "field-class": "ma.fields.Raw",
        }
    }
    marshmallow = {
        "field-class": "ma.fields.Raw",
    }
    json_schema = {"type": "object"}
    mapping = {"enabled": False, "type": "object"}
