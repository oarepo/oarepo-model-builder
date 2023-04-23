from ..datatypes import DataType


class FlattenDataType(DataType):
    # marshmallow_field = "ma_fields.Raw"
    # ui_marshmallow_field = "ma_fields.Raw"
    model_type = "flattened"

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     return []

    # def prepare(self, context):
    #     # not indexing for now as
    #     mapping = self.definition.setdefault("mapping", {})
    #     mapping.setdefault("enabled", False)
    #     super().prepare(context)
