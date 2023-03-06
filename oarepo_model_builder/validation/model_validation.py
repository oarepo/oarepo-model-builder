from collections import defaultdict
from functools import cached_property

import importlib_metadata
import marshmallow as ma
from marshmallow.exceptions import ValidationError

from oarepo_model_builder.validation.utils import PermissiveSchema

PROPERTY_BY_TYPE_PREFIX = "property-by-type-"
ARRAY_ITEM_BY_TYPE_PREFIX = "array-item-by-type-"


class ModelValidator:
    @cached_property
    def validator_map(self):
        ret = {}
        for ep in importlib_metadata.entry_points().select(
            group="oarepo_model_builder.validation"
        ):
            validators = ep.load()
            for validator_type, validator in validators.items():
                ret.setdefault(
                    validator_type, []
                )  # create always, regardless if the validator is empty or not - to register empty extension points
                if isinstance(validator, (list, tuple)):
                    ret[validator_type].extend(validator)
                else:
                    ret[validator_type].append(validator)
        return ret

    def validator_class(self, section="root", strict=True):
        if section.startswith(PROPERTY_BY_TYPE_PREFIX):
            validators = self.get_property_validator_class(section)
        elif section.startswith(ARRAY_ITEM_BY_TYPE_PREFIX):
            validators = self.get_array_item_validator_class(section)
        else:
            validators = tuple(
                self.validator_map[section],
            )

        if not validators:
            return PermissiveSchema

        # if any of the validators is extremely permissive, do not add strict meta
        parent_meta_classes = set()
        for v in validators:
            if hasattr(v, "Meta"):
                parent_meta_classes.add(v.Meta)
                if getattr(v.Meta, "unknown", None) == ma.INCLUDE:
                    strict = False
                    break
        meta_options = {}
        if strict:
            meta_options["unknown"] = ma.RAISE

        # join fields
        fields = defaultdict(list)
        for cls in validators:
            for fld_key, fld in cls._declared_fields.items():
                fields[fld_key].append(fld)
        redefined_fields = {}
        for fld_key, flds in fields.items():
            if len(flds) > 1:
                redefined = self._merge_fields(flds)
                if redefined:
                    redefined_fields[fld_key] = redefined

        meta_class = type("Meta", tuple(parent_meta_classes), meta_options)
        return type(
            f"{section.title()}Validator",
            validators,
            {"Meta": meta_class, **redefined_fields},
        )

    def _merge_fields(self, flds):
        if isinstance(flds[0], ma.fields.Nested):
            schemas = [x.schema for x in flds]
            combined_schema = type(
                "_".join(type(x).__name__ for x in schemas),
                tuple(type(x) for x in schemas),
                {},
            )
            return ma.fields.Nested(
                combined_schema,
                data_key=flds[0].data_key,
                many=flds[0].many,
                attribute=flds[0].attribute,
                allow_none=flds[0].allow_none,
            )
        else:
            return None

    def get_property_validator_class(self, section):
        datatype_name = section[len(PROPERTY_BY_TYPE_PREFIX) :]
        return self._get_datatype_validator_class(
            section, datatype_name, "object-property"
        )

    def get_array_item_validator_class(self, section):
        datatype_name = section[len(ARRAY_ITEM_BY_TYPE_PREFIX) :]
        return self._get_datatype_validator_class(section, datatype_name, "array-item")

    def _get_datatype_validator_class(
        self, section, datatype_name, extra_validation_key
    ):
        from oarepo_model_builder.datatypes import datatypes
        from oarepo_model_builder.datatypes import ObjectDataType

        validators = self.validator_map.get(section, ())

        datatype_class = datatypes.get_datatype_class(datatype_name)
        if not datatype_class:
            raise ValidationError(
                f"No datatype class registered for datatype {datatype_name}"
            )
        validators = tuple(
            [
                *validators,
                *self.validator_map["property"],
                *self.validator_map[extra_validation_key],
                datatype_class.ModelSchema,
            ]
        )
        return validators

    def validate(self, data):
        validator_class = self.validator_class()
        validator = validator_class()
        return validator.dump(validator.load(data))


model_validator = ModelValidator()
