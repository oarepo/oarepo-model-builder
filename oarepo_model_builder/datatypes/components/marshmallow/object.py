import marshmallow as ma
from marshmallow import fields
import dataclasses
from typing import List

from oarepo_model_builder.datatypes import ObjectDataType, datatypes
from oarepo_model_builder.utils.absolute_class import convert_to_absolute_class_name
from oarepo_model_builder.utils.python_name import convert_name_to_python_class
from oarepo_model_builder.validation import InvalidModelException
from oarepo_model_builder.validation.utils import ImportSchema
from .field import (
    PropertyMarshmallowSchema,
    RegularMarshmallowComponent,
    MarshmallowField,
    Import,
)
from .graph import MarshmallowClass


class ExtraField(ma.Schema):
    name = fields.String(required=True)
    value = fields.String(required=True)


class ObjectMarshmallowExtraSchema(ma.Schema):
    imports = fields.List(
        fields.Nested(ImportSchema), required=False
    )  # imports must be here as well as it is used on model's root (without field)
    generate = fields.Boolean(required=False)
    schema_class = fields.String(
        data_key="schema-class",
        attribute="schema-class",
        required=False,
        allow_none=True,
    )
    base_classes = fields.List(
        fields.String(),
        data_key="base-classes",
        attribute="base-classes",
        required=False,
    )
    extra_fields = fields.List(
        fields.Nested(ExtraField),
        required=False,
        data_key="extra-fields",
        attribute="extra-fields",
    )


class ObjectMarshmallowSchema(PropertyMarshmallowSchema, ObjectMarshmallowExtraSchema):
    pass


class ObjectMarshmallowMixin:
    def _register_class_name(
        self, datatype, marshmallow_config, classes, marshmallow_package
    ):
        schema_class = marshmallow_config.get("schema-class")
        if not schema_class:
            return
        schema_class = convert_to_absolute_class_name(schema_class, marshmallow_package)
        classes[schema_class].append(
            (datatype, marshmallow_config.get("generate", True))
        )

    def _build_class_name(
        self,
        datatype,
        marshmallow_config,
        classes,
        marshmallow_package,
        fingerprint,
        suffix,
    ):
        schema_class = marshmallow_config.get("schema-class")

        if schema_class:
            if fingerprint not in classes:
                classes[fingerprint] = schema_class
            return

        schema_class = classes.get(fingerprint)
        if schema_class:
            # reuse, do not generate again
            marshmallow_config["generate"] = False
        else:
            schema_class = self._find_unique_schema_class(
                datatype, classes, marshmallow_package, suffix
            )
            marshmallow_config["generate"] = True
            classes[fingerprint] = schema_class

        marshmallow_config["schema-class"] = schema_class
        classes[schema_class].append((datatype, marshmallow_config["generate"]))

    def _find_unique_schema_class(self, datatype, classes, marshmallow_package, suffix):
        schema_class_list = []

        while datatype:
            if not datatype.key:
                datatype = datatype.parent
                continue

            schema_class_list.insert(0, datatype.key)
            schema_class = (
                convert_name_to_python_class("-".join(x for x in schema_class_list))
                + suffix
            )
            schema_class = convert_to_absolute_class_name(
                schema_class, marshmallow_package
            )
            if schema_class not in classes:
                return schema_class

        # generate unique class name (if duplicates are found) by appending a number
        class_name = schema_class[: -len(suffix)]
        for i in range(1, 100):
            schema_class = f"{class_name}{i}{suffix}"
            if schema_class not in classes:
                return schema_class

        raise InvalidModelException(
            f"Too many marshmallow classes with name {class_name}{suffix}, defined on path {datatype.path}. "
            "Please specify your own class name for marshmallow at this path"
        )

    def _build_class(self, datatype, marshmallow, children, field_generator, classes):
        fields = []
        for _, c in sorted(children.items()):
            datatypes.call_components(c, field_generator, fields=fields)
        extra_fields = [
            MarshmallowField(f["name"], f["value"])
            for f in marshmallow.get("extra-fields", [])
        ]
        classes.append(
            MarshmallowClass(
                class_name=marshmallow["schema-class"],
                base_classes=marshmallow.get("base-classes", []),
                imports=Import.from_config(marshmallow.get("imports", [])),
                fields=[*fields, *extra_fields],
                strict=True,
            )
        )


class ObjectMarshmallowComponent(ObjectMarshmallowMixin, RegularMarshmallowComponent):
    eligible_datatypes = [ObjectDataType]

    class ModelSchema(ma.Schema):
        marshmallow = ma.fields.Nested(ObjectMarshmallowSchema)

    def marshmallow_register_class_names(
        self, *, datatype, classes, marshmallow_package, **kwargs
    ):
        self._register_class_name(
            datatype, datatype.section_marshmallow.config, classes, marshmallow_package
        )

    def marshmallow_build_class_name(
        self, *, datatype, classes, marshmallow_package, **kwargs
    ):
        self._build_class_name(
            datatype,
            datatype.section_marshmallow.config,
            classes,
            marshmallow_package,
            datatype.section_marshmallow.fingerprint,
            "Schema",
        )

    def marshmallow_build_class(self, *, datatype, classes, **kwargs):
        self._build_class(
            datatype,
            datatype.section_marshmallow.config,
            datatype.section_marshmallow.children,
            "marshmallow_field",
            classes,
        )
