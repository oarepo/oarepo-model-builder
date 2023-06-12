from marshmallow import fields

from ..datatypes import DataType
from .object import FieldSchema


class ArrayDataType(DataType):
    model_type = "array"

    ui = {
        "marshmallow": {
            "field-class": "ma.fields.List",
        }
    }
    marshmallow = {
        "field-class": "ma.fields.List",
    }
    json_schema = {"type": "array"}

    class ModelSchema(DataType.ModelSchema):
        items = fields.Nested(FieldSchema)
        uniqueItems = fields.Boolean(required=False)
        minItems = fields.Integer(required=False)
        maxItems = fields.Integer(required=False)

    def prepare(self, context):
        from ..datatypes import datatypes

        items = self.definition.get("items", {})
        self.item = datatypes.get_datatype(self, items, None, self.model, self.schema)
        self.item.prepare(context)
        super().prepare(context)

    def deep_iter(self):
        yield from super().deep_iter()
        yield from self.item.deep_iter()
