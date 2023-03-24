import json
import logging
from hashlib import sha256

from marshmallow import fields

from oarepo_model_builder.utils.jinja import split_package_base_name, split_package_name
from oarepo_model_builder.utils.python_name import convert_name_to_python_class
from oarepo_model_builder.validation import InvalidModelException, model_validator

from .datatypes import DataType

log = logging.getLogger("datatypes")


class ObjectDataType(DataType):
    schema_type = "object"
    mapping_type = "object"
    marshmallow_field = "ma_fields.Nested"
    ui_marshmallow_field = "ma_fields.Nested"
    model_type = "object"

    class ModelSchema(DataType.ModelSchema):
        properties = fields.Nested(
            lambda: model_validator.validator_class("properties", strict=False)()
        )

    def prepare(self, context):
        super().prepare(context)
        self._prepare_schema_class(
            self.definition.setdefault("marshmallow", {}),
            split_package_name(self.model.record_schema_class),
            context,
        )
        ui = self.definition.setdefault("ui", {})
        self._prepare_schema_class(
            ui.setdefault("marshmallow", {}),
            split_package_name(self.model.record_ui_schema_class),
            context,
            suffix="UISchema",
        )

    def _prepare_schema_class(
        self,
        marshmallow_definition,
        package_name,
        context,
        suffix="Schema",
    ):
        if 'schema-class' in marshmallow_definition and marshmallow_definition['schema-class'] is None:
            return
        schema_class = marshmallow_definition.get("schema-class", None)
        if schema_class:
            absolute_class_name = self._get_class_name(package_name, schema_class)
            marshmallow_definition["schema-class"] = absolute_class_name
            return

        if not schema_class:
            if self.stack.top.schema_element_type == "items":
                schema_class_base = self.stack[-2].key + "Item"
            else:
                schema_class_base = self.key
            schema_class = convert_name_to_python_class(schema_class_base) + suffix

        schema_class = self._get_class_name(package_name, schema_class)

        fingerprint = sha256(
            json.dumps(
                self.definition, sort_keys=True, default=lambda x: repr(x)
            ).encode("utf-8")
        ).hexdigest()

        # separate ui and normal marshmallow classes
        class_cache = context.setdefault(f"marshmallow-class-cache-{suffix}", {})

        schema_class = self._find_unique_schema_class(
            class_cache, schema_class, fingerprint
        )
        log.debug(
            "%s: fp %s, schema class %s", self.stack.path, fingerprint, schema_class
        )

        class_cache[schema_class] = fingerprint

        marshmallow_definition["schema-class"] = schema_class

        return marshmallow_definition

    def _find_unique_schema_class(self, known_classes, schema_class, fingerprint):
        parent = self.stack[:-1]
        package_name, class_name = split_package_base_name(schema_class)
        orig_schema_class = schema_class

        # generate unique class name (if duplicates are found) by using more and more from the path
        while True:
            if schema_class not in known_classes:
                # first occurrence, just return
                return schema_class
            if known_classes[schema_class] == fingerprint:
                # same name and fingerprint, just return
                return schema_class
            if not parent:
                # could not resolve parent
                break
            top = parent[-1]
            parent = parent[:-1]
            # if top is not property, can't add to name, so continue with its parent
            if top.schema_element_type != "property":
                continue
            class_name = convert_name_to_python_class(top.key) + class_name
            schema_class = f"{package_name}.{class_name}"

        # generate unique class name (if duplicates are found) by appending a number
        package_name, class_name = split_package_base_name(orig_schema_class)
        for i in range(1, 100):
            schema_class = f"{package_name}.{class_name}{i}"
            if schema_class not in known_classes:
                # first occurrence, just return
                return schema_class
            if known_classes[schema_class] == fingerprint:
                # same name and fingerprint, just return
                return schema_class

        raise InvalidModelException(
            f"Too many marshmallow classes with name {schema_class}. Please specify your own class names"
        )

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
    ui_marshmallow_field = "ma_fields.Nested"
    model_type = "nested"

    def get_facet(self, stack, parent_path):
        if not stack:
            return None
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + "." + self.key
        elif self.key:
            path = self.key
        facet_obj = stack[0].get_facet(stack[1:], path)

        nested_arr = []
        for f in facet_obj:
            nested_arr.append(
                {
                    "facet": f'NestedLabeledFacet(path ="{path}", nested_facet = {f["facet"]})',
                    "path": f["path"],
                }
            )
        return nested_arr


class FlattenDataType(DataType):
    schema_type = "object"
    mapping_type = "object"
    marshmallow_field = "ma_fields.Raw"
    ui_marshmallow_field = "ma_fields.Raw"
    model_type = "flattened"

    def get_facet(self, stack, parent_path):
        pass

    def prepare(self, context):
        # not indexing for now as
        mapping = self.definition.setdefault("mapping", {})
        mapping.setdefault("enabled", False)
        super().prepare(context)


class ArrayDataType(DataType):
    schema_type = "array"
    mapping_type = None
    marshmallow_field = "ma_fields.List"
    ui_marshmallow_field = "ma_fields.List"
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
