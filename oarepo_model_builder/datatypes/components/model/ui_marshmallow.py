from oarepo_model_builder.datatypes import ModelDataType

from ..marshmallow import UIObjectMarshmallowComponent
from .marshmallow import MarshmallowModelMixin


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

    def before_model_prepare(self, datatype, **kwargs):
        record_prefix = datatype.definition["record-prefix"]
        services_module = datatype.definition["record-services-module"]

        default_schema_class = f"{services_module}.schema.{record_prefix}RecordUISchema"

        deepmerge(
            set_default(datatype, "marshmallow", "ui", {}),
            {"schema-class": default_schema_class, "generate": True, "extra-code": ""},
        )
        set_default(datatype, "marshmallow", "base-classes", ["InvenioUISchema"]),

        if "properties" in datatype.definition and "metadata" in (
            datatype.definition["properties"] or {}
        ):
            default_metadata_class = (
                f"{services_module}.schema.{record_prefix}MetadataSchema"
            )
            deepmerge(
                set_default(
                    datatype, "properties", "metadata", "ui", "marshmallow", {}
                ),
                {
                    "schema-class": default_metadata_class,
                    "generate": True,
                },
            )
            set_default(
                datatype,
                "properties",
                "metadata",
                "ui",
                "marshmallow",
                "base-classes",
                ["ma.Schema"],
            ),
