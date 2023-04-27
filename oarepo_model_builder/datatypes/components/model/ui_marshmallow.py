

from oarepo_model_builder.datatypes import ModelDataType

from ..marshmallow import ObjectMarshmallowExtraSchema, UIObjectMarshmallowComponent
from .marshmallow import MarshmallowModelMixin

ModelMarshmallowSchema = ObjectMarshmallowExtraSchema


class UIMarshmallowModelComponent(MarshmallowModelMixin, UIObjectMarshmallowComponent):
    eligible_datatypes = [ModelDataType]
    model_marshmallow_class_name = "record-ui-schema-class"
    context_registered_classes_name = "ui-marshmallow-classes"
    register_class_names_method = "ui_marshmallow_register_class_name"
    build_class_names_existing_method = "ui_marshmallow_build_class_name_existing"
    build_class_names_new_method = "ui_marshmallow_build_class_name_new"

    def ui_marshmallow_register_class_names(self, *, datatype, classes, **kwargs):
        classes[datatype.definition[self.model_marshmallow_class_name]].append(
            (True, datatype)
        )
