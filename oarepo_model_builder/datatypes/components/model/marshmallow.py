from collections import defaultdict

import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType, datatypes

from ..marshmallow import ObjectMarshmallowComponent, ObjectMarshmallowExtraSchema

ModelMarshmallowSchema = ObjectMarshmallowExtraSchema


class MarshmallowModelMixin:
    model_marshmallow_class_name = None
    context_registered_classes_name = None
    register_class_names_method = None
    build_class_names_method = None

    def after_model_prepare(self, *, datatype, context, **kwargs):
        classes = defaultdict(list)
        marshmallow_package = datatype.definition[
            self.model_marshmallow_class_name
        ].rsplit(".", maxsplit=1)[0]
        for node in datatype.deep_iter():
            datatypes.call_components(
                node,
                self.register_class_names_method,
                classes=classes,
                marshmallow_package=marshmallow_package,
            )
        for node in datatype.deep_iter():
            datatypes.call_components(
                node,
                self.build_class_names_existing_method,
                classes=classes,
                marshmallow_package=marshmallow_package,
            )
        for node in datatype.deep_iter():
            datatypes.call_components(
                node,
                self.build_class_names_new_method,
                classes=classes,
                marshmallow_package=marshmallow_package,
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
