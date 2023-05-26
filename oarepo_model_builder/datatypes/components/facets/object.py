from oarepo_model_builder.datatypes import ObjectDataType, datatypes
from oarepo_model_builder.utils.facet_helpers import flatten

from . import FacetDefinition
from .field import RegularFacetsComponent


class ObjectFacetsComponent(RegularFacetsComponent):
    eligible_datatypes = [ObjectDataType]

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
