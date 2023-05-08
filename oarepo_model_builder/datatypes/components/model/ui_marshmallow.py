from typing import Dict

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.utils.python_name import (
    convert_config_to_qualified_name,
    parent_module,
)

from ..marshmallow import UIObjectMarshmallowComponent
from .defaults import DefaultsModelComponent
from .marshmallow import MarshmallowModelMixin
from .service import ServiceModelComponent
from .utils import set_default


class UIMarshmallowModelComponent(MarshmallowModelMixin, UIObjectMarshmallowComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, ServiceModelComponent]
    model_marshmallow_section = ["ui", "marshmallow"]
    context_registered_classes_name = "ui-marshmallow-classes"
    register_class_names_method = "ui_marshmallow_register_class_name"
    build_class_names_existing_method = "ui_marshmallow_build_class_name_existing"
    build_class_names_new_method = "ui_marshmallow_build_class_name_new"

    def ui_marshmallow_register_class_names(self, *, datatype, classes, **kwargs):
        classes[datatype.definition[self.model_marshmallow_class_name]].append(
            (True, datatype)
        )

    def before_model_prepare(self, datatype, **kwargs):
        prefix = datatype.definition["module"]["prefix"]
        services_module = parent_module(datatype.definition["service"]["module"])

        marshmallow: Dict = set_default(datatype, "ui", "marshmallow", {})
        marshmallow.setdefault("generate", True)
        module = marshmallow.setdefault("module", f"{services_module}.ui_schema")
        marshmallow.setdefault("class", f"{module}.{prefix}UISchema")
        marshmallow.setdefault("extra-code", "")
        marshmallow.setdefault("base-classes", ["InvenioUISchema"])
        marshmallow.setdefault(
            "imports", [{"import": "oarepo_runtime.ui.marshmallow.InvenioUISchema"}]
        )
        convert_config_to_qualified_name(marshmallow)

        if "properties" in datatype.definition and "metadata" in (
            datatype.definition["properties"] or {}
        ):
            metadata_marshmallow = set_default(
                datatype, "properties", "metadata", "ui", "marshmallow", {}
            )
            metadata_marshmallow.setdefault("generate", True)
            metadata_module = metadata_marshmallow.setdefault("module", module)
            metadata_marshmallow.setdefault(
                "class", f"{metadata_module}.{prefix}MetadataUISchema"
            )
            metadata_marshmallow.setdefault("extra-code", "")
            metadata_marshmallow.setdefault("base-classes", ["ma.Schema"])
            convert_config_to_qualified_name(metadata_marshmallow)
