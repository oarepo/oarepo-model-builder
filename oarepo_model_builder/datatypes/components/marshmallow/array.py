from typing import List

from ...containers.array import ArrayDataType
from ...datatypes import DataType, Section, datatypes
from .field import RegularMarshmallowComponent
from .graph import MarshmallowField


class ArrayMarshmallowComponent(RegularMarshmallowComponent):
    eligible_datatypes = [ArrayDataType]

    def marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        f = []
        section = datatype.section_marshmallow
        datatypes.call_components(section.item, "marshmallow_field", fields=f)
        item_field: MarshmallowField = f[0]
        f = []
        super().marshmallow_field(datatype, fields=f, item_field=item_field)
        fld: MarshmallowField = f[0]
        fld.imports.extend(item_field.imports)
        fld.reference = item_field.reference
        fields.append(fld)

    def _marshmallow_field_arguments(
        self,
        datatype,
        section: Section,
        marshmallow,
        *,
        item_field: MarshmallowField = None,
    ):
        args = [item_field.full_definition]
        args.extend(
            super()._marshmallow_field_arguments(datatype, section, marshmallow)
        )
        return args
