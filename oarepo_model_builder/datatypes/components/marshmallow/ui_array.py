from typing import List

from ... import ArrayDataType
from ...datatypes import DataType
from .array import ArrayMarshmallowComponentMixin
from .graph import MarshmallowField
from .ui_field import UIMarshmallowComponent


class UIArrayMarshmallowComponent(
    ArrayMarshmallowComponentMixin, UIMarshmallowComponent
):
    eligible_datatypes = [ArrayDataType]

    def ui_marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        section = datatype.section_ui
        self._create_marshmallow_field(
            datatype,
            section,
            section.config.setdefault("marshmallow", {}),
            fields,
            field_accessor="ui_marshmallow_field",
            **kwargs,
        )
