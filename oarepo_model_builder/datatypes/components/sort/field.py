import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import DataTypeComponent, datatypes
from oarepo_model_builder.utils.facet_helpers import facet_name
from oarepo_model_builder.validation.utils import StrictSchema


class PropertySortSchema(StrictSchema):
    key = fields.String(required=False)
    order = fields.String(required=False)
    arguments = fields.List(fields.String(), required=False)
    validators = fields.List(fields.String(), required=False)


class FieldSortComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        sortable = ma.fields.Nested(
            PropertySortSchema,
            required=False,
        )

    def create_sort_options(self, datatype, *, context, **kwargs):
        definition = datatype.section_sortable.config
        if definition:
            key = definition.get("key", facet_name(datatype.path))
            path = datatype.path
            order = definition.get("order", "asc")
            if order == "desc":
                path = "-" + path

            return {key: {"fields": [path]}}

    def after_model_prepare(self, datatype, *, context, **kwargs):
        for node in datatype.deep_iter():
            datatypes.call_components(node, "create_sort_options", context=context)
