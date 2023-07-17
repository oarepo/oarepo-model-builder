from typing import List

from oarepo_model_builder.datatypes.containers.array import ArrayDataType
from oarepo_model_builder.datatypes.datatypes import DataType, Section, datatypes

from .field import RegularMarshmallowComponent, RegularMarshmallowComponentMixin
from .graph import MarshmallowField


class ArrayMarshmallowComponentMixin(RegularMarshmallowComponentMixin):
    def _create_marshmallow_field(
        self, datatype, section, marshmallow, fields, field_accessor=None, **kwargs
    ):
        f = []
        datatypes.call_components(section.item, field_accessor, fields=f)
        if not f:
            return

        item_field: MarshmallowField = f[0]
        f = []
        super()._create_marshmallow_field(
            datatype=datatype,
            section=section,
            marshmallow=marshmallow,
            fields=f,
            item_field=item_field,
        )
        if not f:
            return

        fld: MarshmallowField = f[0]
        fld.imports.extend(item_field.imports)
        fld.reference = item_field.reference
        fields.append(fld)

    def _marshmallow_field_arguments(
        self,
        datatype,
        section: Section,
        marshmallow,
        field_name,
        *,
        item_field: MarshmallowField = None,
    ):
        args = [item_field.full_definition]
        args.extend(
            super()._marshmallow_field_arguments(
                datatype, section, marshmallow, field_name
            )
        )
        return args


class ArrayMarshmallowComponent(
    ArrayMarshmallowComponentMixin, RegularMarshmallowComponent
):
    eligible_datatypes = [ArrayDataType]

    def marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        section = datatype.section_marshmallow
        self._create_marshmallow_field(
            datatype,
            section,
            section.config,
            fields,
            field_accessor="marshmallow_field",
            **kwargs,
        )
