from typing import Dict

from oarepo_model_builder.datatypes import DataType

from ..datatypes.components.facets import FacetDefinition
from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordSearchFacetsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_facets"
    section = "facets"
    template = "record-facets"

    def build_node(self, node: DataType):
        # everything is done in finish
        pass

    def finish(self, **extra_kwargs):
        facets = get_distinct_facets(self.current_model)
        package = self.current_model.definition["facets"]["module"]

        imports = []
        for f in facets:
            imports.extend(f.imports)

        return super().finish(
            current_package_name=package,
            facets=facets,
            facet_imports=imports,
            **extra_kwargs,
        )


def get_distinct_facets(current_model):
    facets_dict: Dict[str, FacetDefinition] = {}
    for node in current_model.deep_iter():
        facet: FacetDefinition
        for facet in node.section_facets.config["facets"]:
            if facet.path not in facets_dict:
                facets_dict[facet.path] = facet
    return list(facets_dict.values())
