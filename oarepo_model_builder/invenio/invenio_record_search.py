
from oarepo_model_builder.datatypes import DataType

from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordSearchFacetsBuilder(InvenioBaseClassPythonBuilder):
    # TYPE = "invenio_record_search"
    # class_config = "record-search-options-class"
    template = "record-search-options"

    def build_node(self, node: DataType):
        # everything is done in finish
        pass

    def finish(self, **extra_kwargs):
        self._generate_facets(self.current_model, **extra_kwargs)

    def _generate_facets(self, node: DataType, **extra_kwargs):
        facets = node.definition["config"]["facets"]

        package = node.definition["facets"]["module"]
        search_options_data = []
        python_path = self.class_to_path(f"{package}.facets")
        imports = []
        for f in facets:
            search_options_data.append({f["path"]: f["class"]})
            if "imports" in f:
                for i in f["imports"]:
                    imports.append((i["import"]).rsplit(".", 1))

        imports = list(map(list, set(map(tuple, imports))))
        imports.sort(key=lambda x: (x[0], x[1]))

        self.process_template(
            python_path,
            "record-facets",
            current_package_name=package,
            search_options_data=search_options_data,
            imports=imports,
            **extra_kwargs,
        )
