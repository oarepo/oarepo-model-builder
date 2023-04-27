from typing import List

import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import DataType, ObjectDataType, datatypes
from oarepo_model_builder.utils.absolute_class import convert_to_absolute_class_name
from oarepo_model_builder.utils.python_name import (
    base_name,
    convert_name_to_python_class,
    package_name,
    qualified_name,
)
from oarepo_model_builder.validation import InvalidModelException
from oarepo_model_builder.validation.utils import ImportSchema

from .field import (
    Import,
    MarshmallowField,
    PropertyMarshmallowSchema,
    RegularMarshmallowComponent,
)
from .graph import MarshmallowClass, MarshmallowReference


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
        definition_marshmallow,
        classes,
        marshmallow_package,
        fingerprint,
        suffix,
    ):
        schema_class = marshmallow_config.get("schema-class")
        generate = marshmallow_config.get("generate", True)

        if schema_class:
            qualified_schema_class = qualified_name(marshmallow_package, schema_class)
            if qualified_schema_class != schema_class:
                marshmallow_config["schema-class"] = qualified_schema_class
                definition_marshmallow["schema-class"] = qualified_schema_class
                schema_class = qualified_schema_class
            if not generate:
                if fingerprint not in classes:
                    classes[fingerprint] = schema_class
                return

        fingerprint_schema_class = classes.get(fingerprint)
        if fingerprint_schema_class:
            # reuse, do not generate again, even if schema_class was specified
            schema_class = fingerprint_schema_class
            marshmallow_config["generate"] = False
            definition_marshmallow["generate"] = False
        else:
            schema_class = self._find_unique_schema_class(
                schema_class, datatype, classes, marshmallow_package, suffix
            )
            marshmallow_config["generate"] = True
            definition_marshmallow["generate"] = True
            classes[fingerprint] = schema_class

        marshmallow_config["schema-class"] = schema_class
        definition_marshmallow["schema-class"] = schema_class

        classes[schema_class].append((datatype, marshmallow_config["generate"]))

    def _find_unique_schema_class(
        self, original_schema_class, datatype, classes, marshmallow_package, suffix
    ):
        schema_class_list = []
        if original_schema_class:
            # insert dummy datatype with class name
            datatype = DataType(
                parent=datatype,
                definition={},
                key=base_name(original_schema_class),
                model=datatype.model,
                schema=datatype.schema,
            )
            marshmallow_package = (
                package_name(original_schema_class) or marshmallow_package
            )
            if original_schema_class.endswith(suffix):
                suffix = ""

        while datatype:
            if not datatype.key:
                datatype = datatype.parent
                schema_class_list.insert(0, "Item")
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

            datatype = datatype.parent

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
        fields = [*fields, *extra_fields]
        fields.sort(key=lambda x: (not x.key.startswith("_"), x.key))
        classes.append(
            MarshmallowClass(
                class_name=marshmallow["schema-class"],
                base_classes=marshmallow.get("base-classes", []) or ["ma.Schema"],
                imports=Import.from_config(marshmallow.get("imports", [])),
                fields=fields,
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

    def marshmallow_build_class_name_existing(
        self, *, datatype, classes, marshmallow_package, **kwargs
    ):
        if datatype.section_marshmallow.config.get("schema-class"):
            self._build_class_name(
                datatype,
                datatype.section_marshmallow.config,
                datatype.definition.setdefault("marshmallow", {}),
                classes,
                marshmallow_package,
                datatype.section_marshmallow.fingerprint,
                "Schema",
            )

    def marshmallow_build_class_name_new(
        self, *, datatype, classes, marshmallow_package, **kwargs
    ):
        if not datatype.section_marshmallow.config.get("schema-class"):
            self._build_class_name(
                datatype,
                datatype.section_marshmallow.config,
                datatype.definition.setdefault("marshmallow", {}),
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

    def marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        section = datatype.section_marshmallow
        f = []
        super().marshmallow_field(datatype, fields=f)
        fld: MarshmallowField = f[0]
        fld.reference = MarshmallowReference(reference=section.config["schema-class"])
        fields.append(fld)

    def _marshmallow_field_arguments(self, datatype, section, marshmallow, field_name):
        return [
            "__reference__",
            *super()._marshmallow_field_arguments(
                datatype, section, marshmallow, field_name
            ),
        ]
