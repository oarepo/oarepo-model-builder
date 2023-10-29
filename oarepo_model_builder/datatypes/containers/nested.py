from .object import ObjectDataType


class NestedDataType(ObjectDataType):
    model_type = "nested"

    mapping = {"type": "nested"}
    facets = {
        "facet-class": "oarepo_runtime.facets.nested_facet.NestedLabeledFacet",
    }
