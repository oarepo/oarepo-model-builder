import itertools

import importlib_metadata
import marshmallow as ma


def ExtensibleSchema(extensibility_entry_point, *base_schemas):
    def creator(*args, **kwargs):
        extra_validators = []
        for ep in sorted(
            importlib_metadata.entry_points(
                group=f"oarepo_model_builder.validation.{extensibility_entry_point}"
            ),
            key=lambda x: x.name,
        ):
            extra_validators.append(ep.load())
        name = "_".join(
            x.__name__ for x in itertools.chain(base_schemas, extra_validators)
        )
        return type(name, tuple([*extra_validators, *base_schemas]), {})(
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
