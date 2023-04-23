from ..datatypes import DataType
from marshmallow import fields
from .object import FieldSchema
from .utils import deep_searchable_enabled
from ...utils.deepmerge import deepmerge


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

    def _process_json_schema(self, section, **kwargs):
        section.setdefault("type", "array")
        child_jsonschema = self.item.json_schema
        if "items" in section:
            deepmerge(section["items"], child_jsonschema)
        else:
            section["items"] = child_jsonschema

    def _process_mapping(self, section, **kwargs):
        super()._process_mapping(section, **kwargs)
        section.pop("type")
        if section.get("enabled", None) is False:
            return
        if not deep_searchable_enabled(self):
            section.setdefault("enabled", False)
            return
        child_mapping = self.item.mapping
        deepmerge(section, child_mapping)

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     if not stack:
    #         return None
    #     return super().get_facet(stack, parent_path, path_suffix)

    # def _get_facet_definition(
    #     self, stack, facet_class, facet_name, path, path_suffix, label, serialized_args
    # ):
    #     return stack[0].get_facet(stack[1:], f"{path}{path_suffix}")
