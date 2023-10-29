from collections import defaultdict
from typing import Dict

import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType, datatypes
from oarepo_model_builder.utils.dict import dict_get
from oarepo_model_builder.utils.python_name import (
    convert_config_to_qualified_name,
    parent_module,
)

from ..marshmallow import ObjectMarshmallowComponent, ObjectMarshmallowExtraSchema
from .defaults import DefaultsModelComponent
from .service import ServiceModelComponent
from .utils import set_default


class ModelMarshmallowSchema(ObjectMarshmallowExtraSchema):
    extra_code = ma.fields.String(
        attribute="extra-code",
        data_key="extra-code",
    )


class MarshmallowModelMixin:
    model_marshmallow_section = None
    context_registered_classes_name = None
    register_class_names_method = None
    build_class_names_method = None

    def after_model_prepare(self, *, datatype, **__kwargs):
        classes = defaultdict(list)
        marshmallow_def = dict_get(datatype.definition, self.model_marshmallow_section)
        marshmallow_module = marshmallow_def["module"]

        for node in datatype.deep_iter():
            datatypes.call_components(
                node,
                self.register_class_names_method,
                classes=classes,
                marshmallow_module=marshmallow_module,
            )
        for node in datatype.deep_iter():
            datatypes.call_components(
                node,
                self.build_class_names_existing_method,
                classes=classes,
                marshmallow_module=marshmallow_module,
            )
        for node in datatype.deep_iter():
            datatypes.call_components(
                node,
                self.build_class_names_new_method,
                classes=classes,
                marshmallow_module=marshmallow_module,
            )


class MarshmallowModelComponent(MarshmallowModelMixin, ObjectMarshmallowComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, ServiceModelComponent]

    model_marshmallow_section = ["marshmallow"]
    context_registered_classes_name = "marshmallow-classes"
    register_class_names_method = "marshmallow_register_class_name"
    build_class_names_existing_method = "marshmallow_build_class_name_existing"
    build_class_names_new_method = "marshmallow_build_class_name_new"

    class ModelSchema(ma.Schema):
        marshmallow = ma.fields.Nested(ModelMarshmallowSchema)

    def marshmallow_register_class_names(self, *, datatype, classes, **kwargs):
        marshmallow_def = dict_get(datatype.definition, self.model_marshmallow_section)
        classes[marshmallow_def["class"]].append((True, datatype))

    def before_model_prepare(self, datatype, *, context, **kwargs):
        prefix = datatype.definition["module"]["prefix"]
        services_module = parent_module(datatype.definition["service"]["module"])

        marshmallow: Dict = set_default(datatype, "marshmallow", {})
        marshmallow.setdefault("generate", True)
        module = marshmallow.setdefault("module", f"{services_module}.schema")
        marshmallow.setdefault("class", f"{module}.{prefix}Schema")
        marshmallow.setdefault("extra-code", "")
        marshmallow.setdefault("base-classes", ["marshmallow.Schema"])
        convert_config_to_qualified_name(marshmallow)

        if "properties" in datatype.definition and "metadata" in (
            datatype.definition["properties"] or {}
        ):
            metadata_marshmallow = set_default(
                datatype, "properties", "metadata", "marshmallow", {}
            )
            metadata_module = metadata_marshmallow.setdefault("module", module)
            metadata_marshmallow.setdefault("generate", True)
            metadata_marshmallow.setdefault(
                "class", f"{metadata_module}.{prefix}MetadataSchema"
            )
            metadata_marshmallow.setdefault("extra-code", "")
            metadata_marshmallow.setdefault("base-classes", ["marshmallow.Schema"])
            convert_config_to_qualified_name(metadata_marshmallow)
