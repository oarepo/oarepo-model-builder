import itertools

import importlib_metadata
import marshmallow as ma

from oarepo_model_builder.utils.import_class import import_class


def ExtensibleSchema(  # NOSONAR - title case because used inside a class
    extensibility_entry_point, *base_schemas
):
    def creator(*args, **kwargs):
        extra_validators = []
        for ep in sorted(
            importlib_metadata.entry_points(
                group=f"oarepo_model_builder.validation.{extensibility_entry_point}"
            ),
            key=lambda x: x.name,
        ):
            extra_validators.append(ep.load())
        base_schema_classes = []
        for bs in base_schemas:
            if isinstance(bs, str):
                bs = import_class(bs)
            base_schema_classes.append(bs)
        name = "_".join(
            x.__name__ for x in itertools.chain(base_schema_classes, extra_validators)
        )
        return type(name, tuple([*extra_validators, *base_schema_classes]), {})(
            *args, **kwargs
        )

    creator.__name__ = (
        base_schemas[0].__name__
        if base_schemas
        else f"ExtensibleSchema_{extensibility_entry_point}"
    )
    return creator


class ExtensibleSchemaMetaClass(type(ma.Schema)):
    def __new__(mcs, name, bases, attrs):
        return super().__new__(mcs, name, (*extra_validators, bases), attrs)
