from oarepo_model_builder.datatypes import DataTypeComponent, datatypes


class RegularSortComponent(DataTypeComponent):
    eligible_datatypes = []

    def after_model_prepare(self, datatype, *, context, **kwargs):
        sort_options = []
        for node in datatype.deep_iter():
            sort_data = datatypes.call_components(
                node, "create_sort_options", context=context
            )
            if sort_data[0]:
                sort_options.extend(sort_data)
        datatype.definition["sortable"] = sort_options
