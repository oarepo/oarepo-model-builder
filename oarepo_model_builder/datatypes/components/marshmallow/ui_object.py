from typing import List

from ... import DataType, ObjectDataType
from .graph import MarshmallowField, MarshmallowReference
from .object import ObjectMarshmallowMixin
from .ui_field import UIMarshmallowComponent


class UIObjectMarshmallowComponent(ObjectMarshmallowMixin, UIMarshmallowComponent):
    eligible_datatypes = [ObjectDataType]

    def ui_marshmallow_register_class_names(
        self, *, datatype, classes, marshmallow_module, **__kwargs
    ):
        self._register_class_name(
            datatype,
            datatype.section_ui.config.setdefault("marshmallow", {}),
            classes,
            marshmallow_module,
        )

    def ui_marshmallow_build_class_name_existing(
        self, *, datatype, classes, marshmallow_module, **__kwargs
    ):
        if datatype.section_ui.config.get("marshmallow", {}).get("class"):
            self._build_class_name(
                datatype,
                datatype.section_ui.config.setdefault("marshmallow", {}),
                datatype.definition.setdefault("ui", {}).setdefault("marshmallow", {}),
                classes,
                marshmallow_module,
                datatype.section_ui.fingerprint,
                "UISchema",
            )

    def ui_marshmallow_build_class_name_new(
        self, *, datatype, classes, marshmallow_module, **__kwargs
    ):
        if not datatype.section_ui.config.get("marshmallow", {}).get("class"):
            self._build_class_name(
                datatype,
                datatype.section_ui.config.setdefault("marshmallow", {}),
                datatype.definition.setdefault("ui", {}).setdefault("marshmallow", {}),
                classes,
                marshmallow_module,
                datatype.section_ui.fingerprint,
                "UISchema",
            )

    def ui_marshmallow_build_class(self, *, datatype, classes, **__kwargs):
        self._build_class(
            datatype,
            datatype.section_ui.config.setdefault("marshmallow", {}),
            datatype.section_ui.children,
            "ui_marshmallow_field",
            classes,
            default_base_class=datatype.schema.settings["marshmallow"][
                "ui-schema-base-class"
            ],
        )

    def ui_marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **__kwargs
    ):
        section = datatype.section_ui
        f = []
        super().ui_marshmallow_field(datatype, fields=f)
        if not f:
            return
        fld: MarshmallowField = f[0]
        fld.reference = MarshmallowReference(
            reference=section.config["marshmallow"].get("class")
        )
        fields.append(fld)

    def _marshmallow_field_arguments(self, datatype, section, marshmallow, field_name):
        return [
            "__reference__",
            *super()._marshmallow_field_arguments(
                datatype, section, marshmallow, field_name
            ),
        ]
