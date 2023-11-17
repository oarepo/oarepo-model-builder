from typing import List

import marshmallow as ma
import marshmallow.validate
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
    name = fields.String(required=True, metadata={"doc": "Name (lhs) of the field"})
    value = fields.String(
        required=True, metadata={"doc": "Literal definition (rhs) of the field"}
    )


class ObjectMarshmallowExtraSchema(ma.Schema):
    imports = fields.List(
        fields.Nested(ImportSchema),
        required=False,
        metadata={"doc": "Python imports that will be put to marshmallow file"},
    )  # imports must be here as well as it is used on model's root (without field)
    module = ma.fields.String(metadata={"doc": "Class module"})
    generate = fields.Boolean(
        required=False,
        metadata={"doc": "Generate the marshmallow class (default is true)"},
    )
    schema_class = fields.String(
        data_key="class",
        attribute="class",
        required=False,
        allow_none=True,
        metadata={"doc": "The name of the marshmallow class"},
    )
    base_classes = fields.List(
        fields.String(),
        data_key="base-classes",
        attribute="base-classes",
        required=False,
        metadata={"doc": "List of marshmallow base classes"},
    )
    extra_fields = fields.List(
        fields.Nested(ExtraField),
        required=False,
        data_key="extra-fields",
        attribute="extra-fields",
        metadata={"doc": "Extra fields to generate into the marshmallow class"},
    )
    skip = fields.Boolean()
    unknown = fields.Str(
        validate=[marshmallow.validate.OneOf(["RAISE", "INCLUDE", "EXCLUDE"])],
        default="RAISE",
    )


class ObjectMarshmallowSchema(PropertyMarshmallowSchema, ObjectMarshmallowExtraSchema):
    pass


class ObjectMarshmallowMixin:
    def _register_class_name(
        self, datatype, marshmallow_config, classes, marshmallow_module
    ):
        schema_class = marshmallow_config.get("class")
        if not schema_class:
            return
        schema_class = convert_to_absolute_class_name(schema_class, marshmallow_module)
        classes[schema_class].append(
            (datatype, marshmallow_config.get("generate", True))
        )

    def _build_class_name(
        self,
        datatype,
        marshmallow_config,
        definition_marshmallow,
        classes,
        marshmallow_module,
        fingerprint,
        suffix,
    ):
        schema_class = marshmallow_config.get("class")
        generate = marshmallow_config.get("generate", True)

        if schema_class:
            qualified_schema_class = qualified_name(marshmallow_module, schema_class)
            if qualified_schema_class != schema_class:
                marshmallow_config["class"] = qualified_schema_class
                definition_marshmallow["class"] = qualified_schema_class
                schema_class = qualified_schema_class
            if not generate:
                if fingerprint not in classes:
                    classes[fingerprint] = schema_class
                return
        if marshmallow_config.get("field") and not schema_class and not generate:
            return

        fingerprint_schema_class = classes.get(fingerprint)
        if fingerprint_schema_class:
            # reuse, do not generate again, even if schema_class was specified
            schema_class = fingerprint_schema_class
            marshmallow_config["generate"] = False
            definition_marshmallow["generate"] = False
        else:
            schema_class = self._find_unique_schema_class(
                schema_class, datatype, classes, marshmallow_module, suffix
            )
            marshmallow_config["generate"] = True
            definition_marshmallow["generate"] = True
            classes[fingerprint] = schema_class

        marshmallow_config["class"] = schema_class
        definition_marshmallow["class"] = schema_class

        classes[schema_class].append((datatype, marshmallow_config["generate"]))

    def _find_unique_schema_class(
        self, original_schema_class, datatype, classes, marshmallow_module, suffix
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
            marshmallow_module = (
                package_name(original_schema_class) or marshmallow_module
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
                schema_class, marshmallow_module
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

    def _build_class(
        self,
        datatype,
        marshmallow,
        children,
        field_generator,
        classes,
        default_base_class,  # NOSONAR
    ):
        fields = []
        for _, c in sorted(children.items()):
            datatypes.call_components(c, field_generator, fields=fields)
        extra_fields = [
            MarshmallowField(f["name"], f["value"])
            for f in marshmallow.get("extra-fields", [])
        ]
        fields = [*fields, *extra_fields]
        fields.sort(key=lambda x: (not x.key.startswith("_"), x.key))
        base_classes = marshmallow.get("base-classes", [])
        if not base_classes:
            base_classes = [default_base_class]
        classes.append(
            MarshmallowClass(
                class_name=marshmallow["class"],
                base_classes=base_classes,
                imports=Import.from_config(marshmallow.get("imports", [])),
                fields=fields,
                unknown=marshmallow.get("unknown", "RAISE"),
            )
        )


class ObjectMarshmallowComponent(ObjectMarshmallowMixin, RegularMarshmallowComponent):
    eligible_datatypes = [ObjectDataType]

    class ModelSchema(ma.Schema):
        marshmallow = ma.fields.Nested(ObjectMarshmallowSchema)

    def marshmallow_register_class_names(
        self, *, datatype, classes, marshmallow_module, **kwargs
    ):
        self._register_class_name(
            datatype, datatype.section_marshmallow.config, classes, marshmallow_module
        )

    def marshmallow_build_class_name_existing(
        self, *, datatype, classes, marshmallow_module, **kwargs
    ):
        if datatype.section_marshmallow.config.get("class"):
            self._build_class_name(
                datatype,
                datatype.section_marshmallow.config,
                datatype.definition.setdefault("marshmallow", {}),
                classes,
                marshmallow_module,
                datatype.section_marshmallow.fingerprint,
                "Schema",
            )

    def marshmallow_build_class_name_new(
        self, *, datatype, classes, marshmallow_module, **kwargs
    ):
        if not datatype.section_marshmallow.config.get("class"):
            self._build_class_name(
                datatype,
                datatype.section_marshmallow.config,
                datatype.definition.setdefault("marshmallow", {}),
                classes,
                marshmallow_module,
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
            default_base_class=datatype.schema.settings["marshmallow"][
                "schema-base-class"
            ],
        )

    def marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        section = datatype.section_marshmallow
        f = []
        super().marshmallow_field(datatype, fields=f)
        if not f:
            return
        fld: MarshmallowField = f[0]
        fld.reference = MarshmallowReference(reference=section.config.get("class"))
        fields.append(fld)

    def _marshmallow_field_arguments(self, datatype, section, marshmallow, field_name):
        return [
            "__reference__",
            *super()._marshmallow_field_arguments(
                datatype, section, marshmallow, field_name
            ),
        ]
