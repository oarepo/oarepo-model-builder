import marshmallow as ma
import yaml
from marshmallow import fields
from marshmallow.decorators import PRE_LOAD
from marshmallow.exceptions import ValidationError
from marshmallow_oneofschema import OneOfSchema

from .model_validation import PROPERTY_BY_TYPE_PREFIX, model_validator
from .utils import RegexFieldsSchema


class PropertiesSchema(RegexFieldsSchema):
    class Meta:
        regex_fields = [
            {
                "key": "^.*$",
                "field": lambda: fields.Nested(
                    lambda: model_validator.validator_class("object-field")()
                ),
            },
        ]

    @ma.pre_load(pass_many=False)
    def transform_props_before_load(self, data, **kwargs):
        returned_data = {}
        for k, v in data.items():
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
            returned_data[k] = v
        return returned_data

    def elevate_props(self, v):
        children = {}
        top_props = {}
        for k, v in v.items():
            if k[0] == "^":
                top_props[k[1:]] = v
            else:
                children[k] = v
        return children, top_props


class PropertySchemas:
    def __init__(self, is_array=False) -> None:
        self.is_array = is_array

    def get(self, property_type):
        return model_validator.validator_class(
            f"{PROPERTY_BY_TYPE_PREFIX}{property_type}"
        )


class ObjectFieldSchema(OneOfSchema):
    type_field_remove = False
    type_schemas = PropertySchemas(is_array=False)

    def get_obj_type(self, obj):
        return obj["type"]

    def load(self, data, *, many=None, partial=None, unknown=None, **kwargs):
        # OneOfSchema does not call pre-load actions, so add it here explicitly
        if self._has_processors(PRE_LOAD):
            try:
                processed_data = self._invoke_load_processors(
                    PRE_LOAD, data, many=many, original_data=data, partial=partial
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


class ArrayItemsSchema(ObjectFieldSchema):
    type_schemas = PropertySchemas(is_array=True)
