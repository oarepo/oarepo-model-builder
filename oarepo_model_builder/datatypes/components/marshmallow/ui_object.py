from .ui_field import UIMarshmallowComponent
from .object import (
    ObjectMarshmallowMixin,
    PropertyMarshmallowSchema,
    ObjectMarshmallowSchema,
)
from ... import ObjectDataType, DataType
import marshmallow as ma
from typing import List
from .graph import MarshmallowField, MarshmallowReference


class UIObjectMarshmallowComponent(ObjectMarshmallowMixin, UIMarshmallowComponent):
    eligible_datatypes = [ObjectDataType]

    def ui_marshmallow_register_class_names(
        self, *, datatype, classes, marshmallow_package, **kwargs
    ):
        self._register_class_name(
            datatype,
            datatype.section_ui.config.setdefault("marshmallow", {}),
            classes,
            marshmallow_package,
        )

    def ui_marshmallow_build_class_name_existing(
        self, *, datatype, classes, marshmallow_package, **kwargs
    ):
        if datatype.section_ui.config.get("marshmallow", {}).get("schema-class"):
            self._build_class_name(
                datatype,
                datatype.section_ui.config.setdefault("marshmallow", {}),
                datatype.definition.setdefault("ui", {}).setdefault("marshmallow", {}),
                classes,
                marshmallow_package,
                datatype.section_ui.fingerprint,
                "UISchema",
            )

    def ui_marshmallow_build_class_name_new(
        self, *, datatype, classes, marshmallow_package, **kwargs
    ):
        if not datatype.section_ui.config.get("marshmallow", {}).get("schema-class"):
            self._build_class_name(
                datatype,
                datatype.section_ui.config.setdefault("marshmallow", {}),
                datatype.definition.setdefault("ui", {}).setdefault("marshmallow", {}),
                classes,
                marshmallow_package,
                datatype.section_ui.fingerprint,
                "UISchema",
            )

    def ui_marshmallow_build_class(self, *, datatype, classes, **kwargs):
        self._build_class(
            datatype,
            datatype.section_ui.config.setdefault("marshmallow", {}),
            datatype.section_ui.children,
            "ui_marshmallow_field",
            classes,
        )

    def ui_marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        section = datatype.section_ui
        f = []
        super().ui_marshmallow_field(datatype, fields=f)
        fld: MarshmallowField = f[0]
        fld.reference = MarshmallowReference(
            reference=section.config["marshmallow"]["schema-class"]
        )
        fields.append(fld)

    def _marshmallow_field_arguments(self, datatype, section, marshmallow):
        return [
            "__reference__",
            *super()._marshmallow_field_arguments(datatype, section, marshmallow),
        ]
