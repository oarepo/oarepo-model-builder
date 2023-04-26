from .field import (
    RegularMarshmallowComponent,
    RegularMarshmallowComponentMixin,
    PropertyMarshmallowSchema,
)
from ...datatypes import DataTypeComponent, DataType
import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.validation.utils import StrictSchema
from typing import List
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
            **kwargs
        )
