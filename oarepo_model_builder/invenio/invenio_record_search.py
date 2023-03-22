from oarepo_model_builder.builders import process
from oarepo_model_builder.utils.jinja import package_name

from ..datatypes import datatypes
from ..outputs.json_stack import JSONStack
from ..utils.deepmerge import deepmerge
from .invenio_base import InvenioBaseClassPythonBuilder

OAREPO_FACETS_PROPERTY = "facets"
OAREPO_SORTABLE_PROPERTY = "sortable"


class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search"
    class_config = "record-search-options-class"
    template = None

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.template = "record-search-options"
        self.search_options_data = []
        self.sort_options_data = []
        self.search_options_stack = JSONStack()
        self.facets_definition = []
        self.settings = settings
        if "sortable" in schema.schema:
            self.process_top_sortable(schema.schema["sortable"])
        self.facet_switch = self.schema.model.get("searchable", True)
        self.facet_stack = []

    def finish(self, **extra_kwargs):
        super().finish(
            search_options_data=self.search_options_data,
            facets_definition=self.facets_definition,
            sort_definition=self.sort_options_data,
        )
        python_path = self.class_to_path(self.current_model.record_facets_class)
        self.process_template(
            python_path,
            "record-facets",
            current_package_name=package_name(self.current_model.record_facets_class),
            search_options_data=self.search_options_data,
            **extra_kwargs,
        )

    def process_top_sortable(self, data):
        keys = dir(data)
        for k in keys:
            fields = dir(data[k])
            fields_options = {}
            for field in fields:
                fields_options = deepmerge(fields_options, {field: data[k][field]})
            self.sort_options_data.append({k: fields_options})

    @process("**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        schema_element_type = self.stack.top.schema_element_type
        data = self.stack.top.data
        recurse = True

        if recurse:
            self.build_children()

        if not self.search_options_stack:
            return

        if schema_element_type == "property":
            sort_definition = data.get(OAREPO_SORTABLE_PROPERTY, None)

            if sort_definition != None:
                self.sort_options_data.append(
                    self.process_sort_options(self.stack.path, sort_definition)
                )
        if self.stack.top.schema_element_type in ["property", "items"]:
            d_type = datatypes.get_datatype(
                self.stack.top.data,
                self.stack.top.key,
                self.current_model,
                self.schema,
                self.stack,
            )

            if d_type.get_facet(None, ""):
                stack_data = []
                for s in self.stack.stack:
                    type = s.schema_element_type
                    if type and type == "property":
                        stack_data.append(
                            datatypes.get_datatype(
                                s.data,
                                s.key,
                                self.current_model,
                                self.schema,
                                self.stack,
                            )
                        )
                    elif type == "items":
                        stack_data.append(
                            datatypes.get_datatype(
                                s.data,
                                None,
                                self.current_model,
                                self.schema,
                                self.stack,
                            )
                        )
                skip = False

                if self.facet_switch:
                    for s in stack_data:
                        if (
                            "facets" in s.definition
                            and "searchable" in s.definition["facets"]
                            and not s.definition["facets"]["searchable"]
                        ):
                            skip = True
                            break
                else:
                    skip = True
                    for s in stack_data:
                        if "facets" in s.definition:
                            if (
                                "searchable" in s.definition["facets"]
                                and s.definition["facets"]["searchable"]
                            ):
                                skip = False
                                break
                            elif (
                                "key" in s.definition["facets"]
                                or "field" in s.definition["facets"]
                            ):
                                skip = False
                                break

                if not skip:
                    # facet, path = datatypes.facet(stack_data)
                    facet_obj = datatypes.facet(stack_data)
                    for f in facet_obj:
                        facet = f['facet']
                        path = f['path']
                        self.search_options_data.append({path: facet})
                        search_ops_name = "facets." + path
                        self.facets_definition.append({path: search_ops_name})

    def process_name(self, path, type):
        path_array = (path.split("/"))[2:]
        name = path_array[0]
        if len(path_array) == 1:
            return name
        path_array.pop(0)
        last_path = ""
        for path in path_array:
            if last_path != "properties" and path == "items":
                continue
            last_path = path
            if path == "properties":
                continue
            if type == "name":
                name = name + "_" + path
            elif type == "field":
                name = name + "." + path

        return name

    def process_sort_options(self, path, definition):
        field = self.process_name(path=path, type="field")

        key = definition.get("key", "")
        if key == "":
            key = self.process_name(path, "name")
        order = definition.get("order", "asc")
        if order == "desc":
            field = "-" + field

        return {key: dict(fields=[field])}
