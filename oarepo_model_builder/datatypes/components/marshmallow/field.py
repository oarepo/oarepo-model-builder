import dataclasses
from typing import List

import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.validation.utils import ImportSchema, StrictSchema

from ...datatypes import DataType, Import
import copy
from .graph import MarshmallowField


class PropertyMarshmallowSchema(StrictSchema):
    read = fields.Boolean(required=False)
    write = fields.Boolean(required=False)
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    field_name = fields.String(
        data_key="field-name", attribute="field-name", required=False
    )
    field = fields.String(required=False)
    field_class = fields.String(
        data_key="field-class", attribute="field-class", required=False
    )
    arguments = fields.List(fields.String(), required=False)
    validators = fields.List(fields.String(), required=False)


class RegularMarshmallowComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        marshmallow = ma.fields.Nested(
            PropertyMarshmallowSchema,
            required=False,
        )

    def marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        marshmallow = datatype.section_marshmallow.config
        imports = Import.from_config(marshmallow.get("imports", []))
        field = marshmallow.get("field", None)
        if not field:
            field_class = marshmallow.get("field-class")
            if not field_class:
                return
            field_decl = [
                field_class,
                "(",
                ", ".join(
                    self._marshmallow_field_arguments(
                        datatype, datatype.section_marshmallow, marshmallow, **kwargs
                    )
                ),
                ")",
            ]
            field = "".join(field_decl)
        fields.append(
            MarshmallowField(
                marshmallow.get("field-name", datatype.key), field, imports
            )
        )

    def _marshmallow_field_arguments(self, datatype, section, marshmallow):
        arguments = copy.copy(marshmallow.get("arguments", []))
        read = marshmallow.get("read", True)
        write = marshmallow.get("write", True)
        if read and not write:
            arguments.append("dump_only=True")
        elif write and not read:
            arguments.append("load_only=True")

        key = datatype.key
        field_name = marshmallow.get("field-name", datatype.key)

        if key != field_name:
            arguments.append(f'data_key="{key}"')
            arguments.append(f'attribute="{key}"')

        validators = marshmallow.get("validators", [])
        if validators:
            arguments.append(f"validate=[{', '.join(validators)}]")

        return arguments
