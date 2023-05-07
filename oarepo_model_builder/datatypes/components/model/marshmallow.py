from collections import defaultdict

import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType, datatypes

from ..marshmallow import ObjectMarshmallowComponent, ObjectMarshmallowExtraSchema
from .utils import set_default


class ModelMarshmallowSchema(ObjectMarshmallowExtraSchema):
    extra_code = ma.fields.String(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be merged to marshmallow file"},
    )


class MarshmallowModelMixin:
    model_marshmallow_class_name = None
    context_registered_classes_name = None
    register_class_names_method = None
    build_class_names_method = None

    def after_model_prepare(self, *, datatype, context, **kwargs):
        classes = defaultdict(list)
        marshmallow_module = datatype.definition[
            self.model_marshmallow_class_name
        ].rsplit(".", maxsplit=1)[0]
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
    model_marshmallow_class_name = "record-schema-class"
    context_registered_classes_name = "marshmallow-classes"
    register_class_names_method = "marshmallow_register_class_name"
    build_class_names_existing_method = "marshmallow_build_class_name_existing"
    build_class_names_new_method = "marshmallow_build_class_name_new"

    class ModelSchema(ma.Schema):
        marshmallow = ma.fields.Nested(ModelMarshmallowSchema)

    def marshmallow_register_class_names(self, *, datatype, classes, **kwargs):
        classes[datatype.definition[self.model_marshmallow_class_name]].append(
            (True, datatype)
        )

    def before_model_prepare(self, datatype, **kwargs):
        record_prefix = datatype.definition["record-prefix"]
        services_module = datatype.definition["record-services-module"]

        default_schema_class = f"{services_module}.schema.{record_prefix}RecordSchema"

        deepmerge(
            set_default(datatype, "marshmallow", {}),
            {
                "schema-class": default_schema_class,
                "generate": True,
            },
        )
        set_default(datatype, "marshmallow", "base-classes", ["ma.Schema"]),

        if "properties" in datatype.definition and "metadata" in (
            datatype.definition["properties"] or {}
        ):
            default_metadata_class = (
                f"{services_module}.schema.{record_prefix}MetadataSchema"
            )
            deepmerge(
                set_default(datatype, "properties", "metadata", "marshmallow", {}),
                {
                    "schema-class": default_metadata_class,
                    "generate": True,
                    "extra-code": "",
                },
            )
            set_default(
                datatype,
                "properties",
                "metadata",
                "marshmallow",
                "base-classes",
                ["ma.Schema"],
            ),
