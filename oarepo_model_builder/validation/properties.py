import marshmallow as ma
import yaml
from marshmallow import fields
from marshmallow.decorators import PRE_LOAD
from marshmallow.exceptions import ValidationError
from marshmallow_oneofschema import OneOfSchema

from .model_validation import PROPERTY_BY_TYPE_PREFIX, model_validator
from .utils import RegexFieldsSchema




class ArrayItemsSchema(ObjectFieldSchema):
    type_schemas = PropertySchemas(is_array=True)
