import logging

import marshmallow as ma
import yaml
from marshmallow.exceptions import ValidationError
from marshmallow_oneofschema import OneOfSchema

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
        if ma.decorators.PRE_LOAD in self._hooks:
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
        try:
            return super().deserialize(returned_value, attr=attr, data=data, **kwargs)
        except ValidationError as e:
            components = e.messages["components"]
            new_components = components.pop("value", {})
            components.update(new_components)
            raise e

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
    model_type = "object"

    ui = {
        "marshmallow": {
            "field-class": "marshmallow.fields{ma_fields.Nested}",
        }
    }
    marshmallow = {
        "field-class": "marshmallow.fields{ma_fields.Nested}",
    }
    json_schema = {"type": "object"}
    mapping = {"type": "object"}

    class ModelSchema(DataType.ModelSchema):
        properties = ObjectPropertiesField()

        @ma.decorators.pre_load()
        def before_load(self, value, **kwargs):
            if not value:
                return value
            if isinstance(value, dict) and value.get("properties") is None:
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

    def deep_iter(self):
        yield from super().deep_iter()
        for c in self.children.values():
            yield from c.deep_iter()
