from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search_options"
    section = "search-options"
    template = "record-search-options"

    def finish(self, **extra_kwargs):
        facets = self.current_model.definition["config"]["facets"]
        search_data = []
        for f in facets:
            search_data.append({f["path"]: "facets." + f["path"]})
        extra_kwargs["search_data"] = search_data
        super().finish(**extra_kwargs)
