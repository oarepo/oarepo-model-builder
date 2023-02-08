from collections import defaultdict
from functools import cached_property, partial

import importlib_metadata
import marshmallow as ma
from marshmallow.exceptions import ValidationError

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
            raise ValidationError(f'Do not have validators for "{section}"')

        # if any of the validators is extremely permissive, do not add strict meta
        for v in validators:
            if hasattr(v, "Meta"):
                if getattr(v.Meta, "unknown", None) == ma.INCLUDE:
                    strict = False
                    break
        if strict:

            class Meta:
                unknown = ma.RAISE

            return type(f"{section.title()}Validator", validators, {"Meta": Meta})
        else:
            return type(f"{section.title()}Validator", validators, {})

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
