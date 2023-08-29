from oarepo_model_builder.datatypes import StringDataType

from .field import RegularMarshmallowComponent


class StringMarshmallowComponent(RegularMarshmallowComponent):
    eligible_datatypes = [StringDataType]

    def prepare(self, datatype, *, context, **kwargs):
        min_length = datatype.definition.get("minLength", None)
        max_length = datatype.definition.get("maxLength", None)
        if min_length is None and max_length is None:
            return
        m = datatype.definition.setdefault("marshmallow", {})
        validators = m.setdefault("validators", [])
        args = []
        if min_length is not None:
            args.append("min=%s" % min_length)
        if max_length is not None:
            args.append("max=%s" % max_length)
        validators.append("ma.validate.Length(%s)" % ", ".join(args))
