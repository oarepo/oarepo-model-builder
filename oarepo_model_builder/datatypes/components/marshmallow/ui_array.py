from .ui_field import (
    UIMarshmallowComponent,
)
from .array import ArrayMarshmallowComponentMixin
from ...datatypes import DataTypeComponent, DataType
from ... import ArrayDataType
import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.validation.utils import StrictSchema
from typing import List
from .graph import MarshmallowField


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
