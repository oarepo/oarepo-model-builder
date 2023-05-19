from typing import List

from ...datatypes import DataType, DataTypeComponent
from .field import RegularMarshmallowComponentMixin
from .graph import MarshmallowField


class UIMarshmallowComponent(RegularMarshmallowComponentMixin, DataTypeComponent):
    def ui_marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        marshmallow = datatype.section_ui
        self._create_marshmallow_field(
            datatype,
            marshmallow,
            marshmallow.config.setdefault("marshmallow", {}),
            fields,
            **kwargs,
        )
