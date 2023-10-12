import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components.model.utils import set_default


class ExtResourceSchema(ma.Schema):
    generate = ma.fields.Bool()
    skip = ma.fields.Bool()

    class Meta:
        unknown = ma.RAISE


class ExtResourceModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        ext_resource = ma.fields.Nested(
            ExtResourceSchema,
            attribute="ext-resource",
            data_key="ext-resource",
        )

    def process_ext_resource(self, datatype, section, **kwargs):
        if datatype.profile == "record":
            cfg = section.config
            cfg["ext-service-name"] = "service_records"
            cfg["ext-resource-name"] = "resource_records"

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if not datatype.profile == "record":
            return
        ext = set_default(datatype, "ext-resource", {})

        ext.setdefault("generate", True)
        ext.setdefault("skip", False)
