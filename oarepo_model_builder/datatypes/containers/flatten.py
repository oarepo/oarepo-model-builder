from ..datatypes import DataType


class FlattenDataType(DataType):
    model_type = "flattened"

    ui = {
        "marshmallow": {
            "field-class": "ma_fields.Raw",
        }
    }
    marshmallow = {
        "field-class": "ma_fields.Raw",
    }
    json_schema = {"type": "object"}
    mapping = {"enabled": False}

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     return []