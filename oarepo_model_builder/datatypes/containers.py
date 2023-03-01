import json
import logging
from hashlib import sha256

from marshmallow import fields

from oarepo_model_builder.utils.jinja import split_package_name
from oarepo_model_builder.utils.python_name import convert_name_to_python_class
from oarepo_model_builder.validation import InvalidModelException, model_validator

from .datatypes import DataType

log = logging.getLogger("datatypes")


class ObjectDataType(DataType):
    schema_type = "object"
    mapping_type = "object"
    marshmallow_field = "ma_fields.Nested"
    model_type = "object"

    class ModelSchema(DataType.ModelSchema):
        properties = fields.Nested(
            lambda: model_validator.validator_class("properties", strict=False)()
        )

    def marshmallow(self, **extras):
        marshmallow_definition = super().marshmallow(**extras)
        self._extend_marshmallow(
            marshmallow_definition, record_schema_class=self.model.record_schema_class
        )
        return marshmallow_definition

    def ui_marshmallow(self, **extras):
        marshmallow_definition = super().ui_marshmallow(**extras)
        self._extend_marshmallow(
            marshmallow_definition,
            record_schema_class=self.model.record_ui_schema_class,
            suffix="UISchema",
        )
        return marshmallow_definition

    def _extend_marshmallow(
        self, marshmallow_definition, record_schema_class=None, suffix="Schema"
    ):
        schema_class = marshmallow_definition.get("schema-class", None)
        if not schema_class:
            if self.stack.top.schema_element_type == "items":
                schema_class_base = self.stack[-2].key + "Item"
            else:
                schema_class_base = self.key
            schema_class = convert_name_to_python_class(schema_class_base) + suffix

        package_name = split_package_name(record_schema_class)

        schema_class = self._get_class_name(package_name, schema_class)

        fingerprint = sha256(
            json.dumps(
                self.definition, sort_keys=True, default=lambda x: repr(x)
            ).encode("utf-8")
        ).hexdigest()

        if "known-classes" not in self.model:
            self.model.known_classes = {}

        schema_class = self._find_unique_schema_class(
            self.model.known_classes, schema_class, fingerprint
        )
        log.debug(
            "%s: fp %s, schema class %s", self.stack.path, fingerprint, schema_class
        )

        self.model.known_classes[schema_class] = fingerprint

        marshmallow_definition["schema-class"] = schema_class

        return marshmallow_definition

    def _find_unique_schema_class(self, known_classes, schema_class, fingerprint):
        if schema_class in known_classes:
            # reuse class with the same fingerprint
            if fingerprint != known_classes[schema_class]:
                path = []
                for pth in reversed(self.stack.stack[:-1]):
                    if pth.schema_element_type == "property":
                        path.insert(0, pth.key)
                        candidate = self._get_schema_class_candidate(
                            schema_class,
                            fingerprint,
                            prefix="".join(x.title() for x in path),
                            known_classes=known_classes,
                        )
                        if candidate:
                            return candidate
                for i in range(1, 100):
                    candidate = self._get_schema_class_candidate(
                        schema_class,
                        fingerprint,
                        suffix=f"_{i}",
                        known_classes=known_classes,
                    )
                    if candidate:
                        return candidate

                raise InvalidModelException(
                    f"Too many marshmallow classes with name {schema_class}. Please specify your own class names"
                )

        return schema_class

    def _get_schema_class_candidate(
        self, schema_class, fingerprint, suffix="", prefix="", known_classes=None
    ):
        print(" ... trying", schema_class, prefix, suffix)
        pkg_clz = schema_class.rsplit(".", maxsplit=1)
        if len(pkg_clz) > 1:
            pkg, clz = f"{pkg_clz[0]}.", pkg_clz[1]
        else:
            pkg = ""
            clz = pkg_clz[0]

        candidate = f"{pkg}{prefix}{clz}{suffix}".rsplit(".", maxsplit=1)
        if len(candidate) > 1:
            candidate = candidate[0] + "." + convert_name_to_python_class(candidate[1])
        else:
            candidate = convert_name_to_python_class(candidate[0])
        if candidate not in known_classes:
            return candidate
        if fingerprint == known_classes[candidate]:
            return candidate
        return None

    def _get_class_name(self, package_name: str, class_name: str):
        if "." not in class_name:
            return f"{package_name}.{class_name}"
        if class_name.startswith("."):
            package_path = package_name.split(".")
            while class_name.startswith("."):
                if package_path:
                    package_path = package_path[:-1]
                class_name = class_name[1:]
            if package_path:
                class_name = f"{'.'.join(package_path)}.{class_name}"
        return class_name

    def get_facet(self, stack, parent_path):
        if not stack:
            return None
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + "." + self.key
        elif self.key:
            path = self.key
        return stack[0].get_facet(stack[1:], path)


class NestedDataType(ObjectDataType):
    schema_type = "object"
    mapping_type = "nested"
    marshmallow_field = "ma_fields.Nested"
    model_type = "nested"

    def get_facet(self, stack, parent_path):
        if not stack:
            return None
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + "." + self.key
        elif self.key:
            path = self.key
        nested, ch_path = stack[0].get_facet(stack[1:], path)
        return f'NestedLabeledFacet(path ="{path}", nested_facet = {nested})', ch_path


class FlattenDataType(DataType):
    schema_type = "object"
    mapping_type = "flatten"
    marshmallow_field = "ma_fields.Raw"
    model_type = "flatten"

    def get_facet(self, stack, parent_path):
        pass


class ArrayDataType(DataType):
    schema_type = "array"
    mapping_type = None
    marshmallow_field = "ma_fields.List"
    model_type = "array"

    class ModelSchema(DataType.ModelSchema):
        items = fields.Nested(
            lambda: model_validator.validator_class("array-items", strict=False)()
        )
        uniqueItems = fields.Boolean(required=False)
        minItems = fields.Integer(required=False)
        maxItems = fields.Integer(required=False)

    def get_facet(self, stack, parent_path):
        if not stack:
            return None
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + "." + self.key
        elif self.key:
            path = self.key
        return stack[0].get_facet(stack[1:], path)
