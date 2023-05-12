from .object import ObjectDataType


class NestedDataType(ObjectDataType):
    model_type = "nested"

    mapping = {"type": "nested"}

    facets = {"facet_class": "NestedLabeledFacet"}