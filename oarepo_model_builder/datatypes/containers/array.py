from marshmallow import fields

from ..datatypes import DataType
from .object import FieldSchema


class ArrayDataType(DataType):
    schema_type = "array"
    # marshmallow_field = "ma_fields.List"
    # ui_marshmallow_field = "ma_fields.List"
    model_type = "array"

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

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     if not stack:
    #         return None
    #     return super().get_facet(stack, parent_path, path_suffix)

    # def _get_facet_definition(
    #     self, stack, facet_class, facet_name, path, path_suffix, label, serialized_args
    # ):
    #     return stack[0].get_facet(stack[1:], f"{path}{path_suffix}")
