import logging

import marshmallow as ma
import yaml
from marshmallow import fields
from marshmallow.exceptions import ValidationError
from marshmallow_oneofschema import OneOfSchema

from oarepo_model_builder.validation.utils import ImportSchema
from ..datatypes import DataType

log = logging.getLogger("datatypes")


class PropertySchemas:
    def __init__(self, is_array=False) -> None:
        self.is_array = is_array

    def get(self, property_type):
        from ..datatypes import datatypes

        datatype = datatypes.get_datatype_class(property_type)
        if not datatype:
            raise ma.exceptions.ValidationError(
                f"No datatype registered for {property_type}"
            )
        return datatype.validator


class FieldSchema(OneOfSchema):
    type_field_remove = False
    type_schemas = PropertySchemas(is_array=False)

    def get_obj_type(self, obj):
        return obj["type"]

    def load(self, data, *, many=None, partial=None, unknown=None, **kwargs):
        # OneOfSchema does not call pre-load actions, so add it here explicitly
        if self._has_processors(ma.decorators.PRE_LOAD):
            try:
                processed_data = self._invoke_load_processors(
                    ma.decorators.PRE_LOAD,
                    data,
                    many=many,
                    original_data=data,
                    partial=partial,
                )
            except ValidationError as err:
                errors = err.normalized_messages()
                exc = ValidationError(errors, data=data, valid_data={})
                self.handle_error(exc, data, many=many, partial=partial)
                raise exc
        else:
            processed_data = data

        return super().load(
            processed_data, many=many, partial=partial, unknown=unknown, **kwargs
        )

    @ma.pre_load(pass_many=False)
    def set_type(self, data, **kwargs):
        if not isinstance(data, dict):
            raise ValidationError(f'Must be an object, is "{repr(data)[:20]}..."')
        if "type" not in data:
            if "properties" in data:
                data["type"] = "object"
            if "items" in data:
                data["type"] = "array"
        return data


class ObjectPropertiesField(ma.fields.Dict):
    def __init__(self, **kwargs):
        super().__init__(
            keys=ma.fields.Str(), values=ma.fields.Nested(FieldSchema), **kwargs
        )

    def deserialize(self, value, attr=None, data=None, **kwargs):
        if value is ma.missing:
            value = {}
        if not isinstance(value, dict):
            raise ma.exceptions.ValidationError(
                "Object properties field must be a mapping"
            )
        returned_value = {}
        for k, v in value.items():
            if isinstance(v, str):
                # single-line type followed by yaml => read it
                if "{" not in v:
                    v = {"type": v}
                else:
                    datatype, constraints = v.split("{", maxsplit=1)
                    constraints = constraints.replace(":", ": ")
                    v = {
                        "type": datatype,
                        **yaml.safe_load("blah: {" + constraints)["blah"],
                    }
            if k.endswith("{}"):
                k = k[:-2]
                children, top_props = self.elevate_props(v)
                v = {"type": "object", **top_props, "properties": children}
            if k.endswith("{nested}"):
                k = k[:-8]
                children, top_props = self.elevate_props(v)
                v = {"type": "nested", **top_props, "properties": children}
            if k.endswith("[]"):
                k = k[:-2]
                children, top_props = self.elevate_props(v)
                v = {"type": "array", **top_props, "items": children}
            returned_value[k] = v
        return super().deserialize(returned_value, attr=attr, data=data, **kwargs)

    def elevate_props(self, v):
        children = {}
        top_props = {}
        for k, v in v.items():
            if k[0] == "^":
                top_props[k[1:]] = v
            else:
                children[k] = v
        return children, top_props


class ObjectDataType(DataType):
    schema_type = "object"
    mapping_type = "object"
    # marshmallow_field = "ma_fields.Nested"
    # ui_marshmallow_field = "ma_fields.Nested"
    model_type = "object"

    class ModelSchema(DataType.ModelSchema):
        properties = ObjectPropertiesField()

        @ma.decorators.pre_load()
        def before_load(self, value, **kwargs):
            if not value:
                return value
            if isinstance(value, dict):
                if value.get("properties") is None:
                    value["properties"] = {}
            return value

    def prepare(self, context):
        from ..datatypes import datatypes

        # get children
        properties = self.definition.get("properties", {})
        # children are filled in alphabet order to make them stable
        self.children = {
            k: datatypes.get_datatype(self, v, k, self.model, self.schema)
            for k, v in sorted(properties.items())
        }
        for v in self.children.values():
            v.prepare(context)

        super().prepare(context)

        # self._prepare_schema_class(
        #     self.definition.setdefault("marshmallow", {}),
        #     split_package_name(self.model.record_schema_class),
        #     context,
        # )
        # ui = self.definition.setdefault("ui", {})
        # self._prepare_schema_class(
        #     ui.setdefault("marshmallow", {}),
        #     split_package_name(self.model.record_ui_schema_class),
        #     context,
        #     suffix="UISchema",
        # )

    # def _prepare_schema_class(
    #     self,
    #     marshmallow_definition,
    #     package_name,
    #     context,
    #     suffix="Schema",
    # ):
    #     if (
    #         "schema-class" in marshmallow_definition
    #         and marshmallow_definition["schema-class"] is None
    #     ):
    #         return
    #     schema_class = marshmallow_definition.get("schema-class", None)
    #     if schema_class:
    #         absolute_class_name = self._get_class_name(package_name, schema_class)
    #         marshmallow_definition["schema-class"] = absolute_class_name
    #         return

    #     if not schema_class:
    #         if self.stack.top.schema_element_type == "items":
    #             schema_class_base = self.stack[-2].key + "Item"
    #         else:
    #             schema_class_base = self.key
    #         schema_class = convert_name_to_python_class(schema_class_base) + suffix

    #     schema_class = self._get_class_name(package_name, schema_class)

    #     fingerprint = sha256(
    #         json.dumps(
    #             self.definition, sort_keys=True, default=lambda x: repr(x)
    #         ).encode("utf-8")
    #     ).hexdigest()

    #     # separate ui and normal marshmallow classes
    #     class_cache = context.setdefault(f"marshmallow-class-cache-{suffix}", {})

    #     schema_class = self._find_unique_schema_class(
    #         class_cache, schema_class, fingerprint
    #     )
    #     log.debug(
    #         "%s: fp %s, schema class %s", self.stack.path, fingerprint, schema_class
    #     )

    #     class_cache[schema_class] = fingerprint

    #     marshmallow_definition["schema-class"] = schema_class

    #     return marshmallow_definition

    # def _find_unique_schema_class(self, known_classes, schema_class, fingerprint):
    #     parent = self.stack[:-1]
    #     package_name, class_name = split_package_base_name(schema_class)
    #     orig_schema_class = schema_class

    #     # generate unique class name (if duplicates are found) by using more and more from the path
    #     while True:
    #         if schema_class not in known_classes:
    #             # first occurrence, just return
    #             return schema_class
    #         if known_classes[schema_class] == fingerprint:
    #             # same name and fingerprint, just return
    #             return schema_class
    #         if not parent:
    #             # could not resolve parent
    #             break
    #         top = parent[-1]
    #         parent = parent[:-1]
    #         # if top is not property, can't add to name, so continue with its parent
    #         if top.schema_element_type != "property":
    #             continue
    #         class_name = convert_name_to_python_class(top.key) + class_name
    #         schema_class = f"{package_name}.{class_name}"

    #     # generate unique class name (if duplicates are found) by appending a number
    #     package_name, class_name = split_package_base_name(orig_schema_class)
    #     for i in range(1, 100):
    #         schema_class = f"{package_name}.{class_name}{i}"
    #         if schema_class not in known_classes:
    #             # first occurrence, just return
    #             return schema_class
    #         if known_classes[schema_class] == fingerprint:
    #             # same name and fingerprint, just return
    #             return schema_class

    #     raise InvalidModelException(
    #         f"Too many marshmallow classes with name {schema_class}. Please specify your own class names"
    #     )

    # def _get_class_name(self, package_name: str, class_name: str):
    #     if "." not in class_name:
    #         return f"{package_name}.{class_name}"
    #     if class_name.startswith("."):
    #         package_path = package_name.split(".")
    #         while class_name.startswith("."):
    #             if package_path:
    #                 package_path = package_path[:-1]
    #             class_name = class_name[1:]
    #         if package_path:
    #             class_name = f"{'.'.join(package_path)}.{class_name}"
    #     return class_name

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     if not stack:
    #         return None
    #     return super().get_facet(stack, parent_path, path_suffix)

    # def _get_facet_definition(
    #     self, stack, facet_class, facet_name, path, path_suffix, label, serialized_args
    # ):
    #     return stack[0].get_facet(stack[1:], f"{path}{path_suffix}")
