from oarepo_model_builder.datatypes import NestedDataType

from . import FacetDefinition
from .object import ObjectFacetsComponent


class NestedFacetsComponent(ObjectFacetsComponent):
    eligible_datatypes = [NestedDataType]

    def build_facet_definition(
        self,
        datatype,
        facet_definition: FacetDefinition,
    ):
        facet_section = datatype.section_facets.config

        facet_definition.update(facet_section)
        facet_definition.set_field(
            facet_section,
            arguments=[
                f"path = {repr(datatype.path)}",
                f"nested_facet = {facet_definition.field}",
                *facet_section.get("args", []),
            ],
        )
        return super().build_facet_definition(datatype, facet_definition)

    def process_facets(self, datatype, section, **kwargs):
        # container itself does not generate any facets. Need to have it here because facet-class is set
        # and calling field implementation would generate non meaningful facet record here.
        section.config["facets"] = []
