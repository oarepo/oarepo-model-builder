from ... import NumberDataType
from .field import RegularMarshmallowComponent


class NumberMarshmallowComponent(RegularMarshmallowComponent):
    eligible_datatypes = [NumberDataType]

    def prepare(self, datatype, *, context, **kwargs):
        minimum = datatype.definition.get("minimum", None)
        maximum = datatype.definition.get("maximum", None)
        exclusive_minimum = datatype.definition.get("exclusiveMinimum", None)
        exclusive_maximum = datatype.definition.get("exclusiveMaximum", None)

        if (
            minimum is None
            and maximum is None
            and exclusive_minimum is None
            and exclusive_maximum is None
        ):
            return
        m = datatype.definition.setdefault("marshmallow", {})
        validators = m.setdefault("validators", [])
        args = []

        if minimum is not None:
            args.append("min=%s" % minimum)
        if maximum is not None:
            args.append("max=%s" % maximum)
        if exclusive_minimum is not None:
            args.append("min=%s" % exclusive_minimum)
            args.append("min_inclusive=False")
        if exclusive_maximum is not None:
            args.append("max=%s" % exclusive_maximum)
            args.append("max_inclusive=False")
        validators.append("ma.validate.Range(%s)" % ", ".join(args))
