import copy
from typing import List

import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.utils.python_name import convert_name_to_python
from oarepo_model_builder.validation.utils import ImportSchema, StrictSchema

from ...datatypes import DataType, Import
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


class RegularMarshmallowComponentMixin:
    def _create_marshmallow_field(
        self, datatype, section, marshmallow, fields, **kwargs
    ):
        read = marshmallow.get("read", True)
        write = marshmallow.get("write", True)
        if not read and not write:
            return

        imports = Import.from_config(marshmallow.get("imports", []))
        field = marshmallow.get("field", None)

        key = datatype.key
        if key:
            field_name = marshmallow.get("field-name")
            if not field_name:
                field_name = convert_name_to_python(datatype.key)
                marshmallow["field-name"] = field_name
        else:
            field_name = None

        if not field:
            field_class = marshmallow.get("field-class")
            if not field_class:
                return
            field_decl = [
                field_class,
                "(",
                ", ".join(
                    self._marshmallow_field_arguments(
                        datatype, section, marshmallow, field_name, **kwargs
                    )
                ),
                ")",
            ]
            field = "".join(field_decl)

        fields.append(MarshmallowField(field_name, field, imports))

    def _marshmallow_field_arguments(
        self, datatype, section, marshmallow, field_name  # NOSONAR
    ):
        arguments = copy.copy(marshmallow.get("arguments", []))
        required = datatype.definition.get('required', False)
        if required:
            arguments.append("required=True")
        read = marshmallow.get("read", True)
        write = marshmallow.get("write", True)
        if read and not write:
            arguments.append("dump_only=True")
        elif write and not read:
            arguments.append("load_only=True")

        key = datatype.key

        if key != field_name:
            arguments.append(f'data_key="{key}"')
            arguments.append(f'attribute="{key}"')

        validators = marshmallow.get("validators", [])
        if validators:
            arguments.append(f"validate=[{', '.join(validators)}]")

        return arguments


class RegularMarshmallowComponent(RegularMarshmallowComponentMixin, DataTypeComponent):
    class ModelSchema(ma.Schema):
        marshmallow = ma.fields.Nested(
            PropertyMarshmallowSchema,
            required=False,
        )

    def marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        marshmallow = datatype.section_marshmallow
        self._create_marshmallow_field(
            datatype, marshmallow, marshmallow.config, fields, **kwargs
        )
