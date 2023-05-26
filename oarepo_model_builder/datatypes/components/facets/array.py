from oarepo_model_builder.datatypes import ArrayDataType, datatypes
from oarepo_model_builder.utils.facet_helpers import flatten

from . import FacetDefinition
from .field import RegularFacetsComponent


class ArrayFacetsComponent(RegularFacetsComponent):
    eligible_datatypes = [ArrayDataType]

    def build_facet_definition(
        self,
        datatype,
        facet_definition: FacetDefinition,
    ):
        facet_definition.update(datatype.section_facets.config)
        return flatten(
            datatypes.call_components(
                datatype.parent,
                "build_facet_definition",
                facet_definition=facet_definition,
            )
        )
