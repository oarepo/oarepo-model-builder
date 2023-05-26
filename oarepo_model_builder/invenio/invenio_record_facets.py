from typing import List

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
        facets: List[FacetDefinition] = []
        for node in self.current_model.deep_iter():
            facets.extend(node.section_facets.config["facets"])
        package = self.current_model.definition["facets"]["module"]

        imports = []
        for f in facets:
            imports.extend(f.imports)

        return super().finish(
            current_package_name=package,
            facets=facets,
            imports=imports,
            **extra_kwargs,
        )
