import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import StrictSchema

from .defaults import DefaultsModelComponent
from .utils import set_default


class ProxySchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    module = ma.fields.Str()
    generate = ma.fields.Boolean()


class ProxyModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(StrictSchema):
        proxy = ma.fields.Nested(
            ProxySchema, metadata={"doc": "Settings for service proxy"}
        )

    def before_model_prepare(self, datatype, **kwargs):
        top_module = datatype.definition["module"]["qualified"]
        proxy = set_default(datatype, "proxy", {})
        proxy.setdefault("module", f"{top_module}.proxies")
        proxy.setdefault("generate", True)
