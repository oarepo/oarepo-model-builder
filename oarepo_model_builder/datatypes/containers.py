import json

from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.jinja import split_package_name
from oarepo_model_builder.validation import InvalidModelException, model_validator

from .datatypes import DataType
from marshmallow import fields


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
        ret = super().marshmallow(**extras)

        schema_class = ret.get("schema-class", None)
        if not schema_class:
            schema_class = camel_case(self.key) + "Schema"

        package_name = split_package_name(self.model.record_schema_class)

        schema_class = self._get_class_name(package_name, schema_class)

        fingerprint = json.dumps(
            self.definition, sort_keys=True, default=lambda x: repr(x)
        ).encode("utf-8")

        schema_class = self._find_unique_schema_class(
            self.model.setdefault("known-classes", {}), schema_class, fingerprint
        )

        self.model.known_classes[schema_class] = fingerprint

        ret["schema-class"] = schema_class

        return ret

    def _find_unique_schema_class(self, known_classes, schema_class, fingerprint):
        if schema_class in known_classes:
            # reuse class with the same fingerprint
            if fingerprint != known_classes[schema_class]:
                for i in range(100):
                    candidate = f"{schema_class}_{i}"
                    if candidate not in known_classes:
                        schema_class = candidate
                        break
                    if fingerprint == known_classes[candidate]:
                        schema_class = candidate
                        break
                else:
                    raise InvalidModelException(
                        f"Too many marshmallow classes with name {schema_class}. Please specify your own class names"
                    )

        return schema_class

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

    def facet(self, key, definition= None, props_num = None):
        return {"path": key, "class": "TermFacet", 'props_num' : props_num}

class NestedDataType(ObjectDataType):
    schema_type = "object"
    mapping_type = "nested"
    marshmallow_field = "ma_fields.Nested"
    model_type = "nested"

    def facet(self, key, definition= None, props_num = None):
        print('s')
        return {"path": key, "class": "NestedLabeledFacet", 'props_num' : props_num}



class FlattenDataType(DataType):
    schema_type = "object"
    mapping_type = "flatten"
    marshmallow_field = "ma_fields.Raw"
    model_type = "flatten"

    def facet(self, key, definition= None, props_num = None):
        return {"path": key, "class": "TermFacet", 'props_num' : props_num}

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

    def facet(self, key, definition={}, props_num = None):
        # if 'properties' in definition['items'] or 'items' in definition['items']:
        #     obj = True
        key = definition.get('key', key)
        if key not in definition and 'keyword' in definition:
            key = key + "_keyword"

        field = definition.get('field', "TermsFacet(field = ")
        facet_def = {}
        if 'nested' in definition:
            field = "NestedLabeledFacet"
        elif 'field' in definition:
            facet_def['defined_class'] = True
        facet_def = {"path": key, "class": field}


        if props_num == 0: #todo nested?????? #todo check if facetable
            return False
        if int(props_num or 0) > 1:
            facet_def['props_num'] = props_num
        # if 'simple_array' in definition:
        #     return False #todo simply zero?
        print('facet_def', facet_def)
        return facet_def