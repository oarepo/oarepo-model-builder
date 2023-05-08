from typing import Dict

import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.utils.python_name import parent_module

from ..ui import ObjectUIComponent, ObjectUIExtraSchema
from .marshmallow import ModelMarshmallowSchema
from .resource import ResourceModelComponent
from .utils import set_default


class ModelUISchema(ObjectUIExtraSchema):
    marshmallow = ma.fields.Nested(ModelMarshmallowSchema)
    module = ma.fields.String(
        metadata={"doc": "UI serializer class module"},
    )
    serializer_class = ma.fields.String(
        attribute="serializer-class",
        data_key="serializer-class",
        metadata={"doc": "UI serializer class qualified name"},
    )


class UIModelComponent(ObjectUIComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ResourceModelComponent]

    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(ModelUISchema, metadata={"doc": "UI settings"})

    def before_model_prepare(self, datatype, **kwargs):
        prefix = datatype.definition["module"]["prefix"]
        resources_module = parent_module(datatype.definition["resource"]["module"])

        ui: Dict = set_default(datatype, "ui", {})
        ui_module = ui.setdefault("module", f"{resources_module}.ui")
        ui.setdefault("serializer-class", f"{ui_module}.{prefix}UIJSONSerializer")
