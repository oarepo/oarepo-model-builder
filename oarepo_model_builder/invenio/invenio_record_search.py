from oarepo_model_builder.builders import process
from oarepo_model_builder.utils.jinja import package_name

from ..outputs.json_stack import JSONStack
from ..utils.deepmerge import deepmerge
from ..utils.hyphen_munch import HyphenMunch
from .invenio_base import InvenioBaseClassPythonBuilder

OAREPO_FACETS_PROPERTY = "oarepo:facets"
OAREPO_SORTABLE_PROPERTY = "oarepo:sortable"


class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search"
    class_config = "record-search-options-class"
    template = None

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.template = "record-search-options"
        self.search_options_data = []
        self.sort_options_data = []
        self.search_facets_definiton = []
        self.search_options_stack = JSONStack()
        self.facets_definition = []
        self.facets_names = []
        self.settings = settings
        if "oarepo:sortable" in schema:
            self.process_top_sortable(schema["oarepo:sortable"])

    def finish(self, **extra_kwargs):
        super().finish(
            search_options_data=self.search_options_data,
            facets_definition=self.facets_definition,
            sort_definition=self.sort_options_data,
        )
        python_path = self.class_to_path(self.settings.python["record-facets-class"])
        self.process_template(
            python_path,
            "record-facets",
            current_package_name=package_name(
                self.settings.python["record-facets-class"]
            ),
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

    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        schema_element_type = self.stack.top.schema_element_type

        definition = None
        recurse = True

        if recurse:
            # process children
            self.build_children()

        data = self.stack.top.data

        if not self.search_options_stack:
            return

        if schema_element_type == "property":
            sort_definition = data.get(OAREPO_SORTABLE_PROPERTY, None)

            if sort_definition != None:
                self.sort_options_data.append(
                    self.process_sort_options(self.stack.path, sort_definition)
                )
        array_items_type = None
        if schema_element_type == "property" and data.type == "array":
            try:
                array_items_type = data["items"]["type"]
            except:
                array_items_type = None

        if (
            schema_element_type == "property"
            and data.type != "text"
            and data.type != "fulltext"
            and data.type != "object"
            and data.type != "nested"
            and not (data.type == "array" and array_items_type == "fulltext")
        ):
            definition = data.get(OAREPO_FACETS_PROPERTY, {})
            nested_paths = []
            nested_path = ""
            nested = False
            path_stack = self.stack.stack[3:]  # start inside model properties
            for upper in path_stack:
                if upper.key == "properties":
                    continue
                nested_path = nested_path + upper.key + "."
                if (
                    upper.data.get("oarepo:mapping", HyphenMunch({"type": ""})).type
                    == "nested"
                ):
                    nested_paths.append(nested_path)
            if len(nested_paths) > 0:
                nested = True

            if "key" in definition:
                name = definition["key"]
            else:
                name = self.process_name(self.stack.path, type="name")
            if data.type == "fulltext+keyword" and "key" not in definition:
                name = name + "_keyword"
            if name == "$schema":
                name = "_schema"
            if name == "id":
                name = "_id"
            class_string = ""

            if nested:
                class_string = "NestedLabeledFacet("
                for path in nested_paths:
                    if nested_paths[-1] == path:
                        class_string = class_string + "path = " + '"' + path[:-1] + '"'
                    else:
                        class_string = (
                            class_string
                            + "path = "
                            + '"'
                            + path[:-1]
                            + '"'
                            + ", nested_facet = NestedLabeledFacet("
                        )

            if "field" in definition:
                field = definition["field"]
                if nested:
                    class_string = class_string + " , nested_facet =" + field
                    for x in nested_paths:
                        class_string = class_string + ")"
                    self.search_options_data.append({name: class_string})
                else:
                    self.search_options_data.append({name: field})
            else:
                search_data = []
                field = self.process_name(self.stack.path, type="field")
                if data.type == "fulltext+keyword":
                    field = field + ".keyword"
                search_data.append(["field", field])
                facets_class = definition.get("class", "TermsFacet")
                for key, value in definition.items():
                    if "class" != key and "field" != key:
                        search_data.append([key, value])
                if nested:
                    search_options = self.process_search_options(
                        search_data, facets_class
                    )
                    search_options = class_string + " , nested_facet =" + search_options
                    for x in nested_paths:
                        search_options = search_options + ")"

                else:
                    search_options = self.process_search_options(
                        search_data, facets_class
                    )
                self.search_options_data.append({name: search_options})
            facets_name = "facets." + name
            self.facets_definition.append({name: facets_name})

    def process_search_options(self, data, field_class):
        text = ""
        for x in data:
            if text == "":
                text = text + x[0] + ' = "' + x[1] + '"'
            else:
                text = text + ", " + x[0] + ' = "' + x[1] + '"'
        return field_class + "(" + text + ")"

    def process_name(self, path, type):
        path_array = (path.split("/"))[3:]
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
