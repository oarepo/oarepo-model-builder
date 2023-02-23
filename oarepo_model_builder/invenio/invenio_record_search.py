from oarepo_model_builder.builders import process
from oarepo_model_builder.utils.jinja import package_name
from oarepo_model_builder.utils.python_name import convert_name_to_python

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
            try:
                self.definition = data.get(OAREPO_FACETS_PROPERTY, {})
                fd = datatypes.get_datatype(
                    data, data.type, self.current_model, self.schema, self.stack
                )
                ft = False
                if fd.schema_type == "object":
                    properties = data.get("properties", {})
                    ft = fd.facet(
                        key=self.stack.top.key,
                        props_num=self.properties_types(properties),
                        definition=self.definition,
                        create=self.facet_switch,
                    )
                elif fd.schema_type == "array":
                    ft = fd.facet(
                        key=self.stack.top.key,
                        props_num=self.properties_types(data["items"], True),
                        definition=self.definition,
                        create=self.facet_switch,
                    )
                if ft:
                    self.facet_stack.append(ft)
            except:
                pass

            self.build_children()

        if not self.search_options_stack:
            return

        if schema_element_type == "property":
            sort_definition = data.get(OAREPO_SORTABLE_PROPERTY, None)

            if sort_definition != None:
                self.sort_options_data.append(
                    self.process_sort_options(self.stack.path, sort_definition)
                )

        if schema_element_type == "property" and (
            ("type" in data)
            and (
                datatypes.get_datatype(
                    data, data.type, self.current_model, self.schema, self.stack
                ).schema_type
                != "object"
            )
        ):
            d_type = datatypes.get_datatype(
                data, data.type, self.current_model, self.schema, self.stack
            )
            ft = d_type.facet(
                key=self.stack.top.key,
                definition=self.definition,
                create=self.facet_switch,
            )
            if ft and data.type != "array":
                self.facet_stack.append(ft)
            if len(self.facet_stack) > 0:
                facet_def = ""
                facet_name = ""
                facet_path = ""
                nested_count = 0
                for facet in self.facet_stack:
                    facet_name = (
                        facet_name + convert_name_to_python(facet["path"]) + "_"
                    )
                    facet_path = facet_path + facet["path"] + "."
                    if "defined_class" in facet:
                        facet_def = facet_def + facet["class"]
                    elif facet["class"].startswith("Nested"):
                        nested_count += 1
                        facet_def = (
                            facet_def
                            + f'NestedLabeledFacet(path =" {facet_path[:-1]}", nested_facet='
                        )
                    elif "props_num" in facet:
                        pass
                    else:
                        facet_path = (
                            (facet_path[::-1]).replace(
                                "_keyword."[::-1], ".keyword."[::-1], 1
                            )[::-1]
                            if facet_path.endswith("_keyword.")
                            else facet_path
                        )
                        facet_def = facet_def + facet["class"] + f'"{facet_path[:-1]}"'
                        for i in range(0, nested_count):
                            facet_def = facet_def + ")"
                        facet_def = facet_def + ")"
                self.clean_stack()

                facet_name = facet_name[:-1]
                if facet_def:
                    self.search_options_data.append({facet_name: facet_def})
                    search_ops_name = "facets." + facet_name
                    self.facets_definition.append({facet_name: search_ops_name})

    def process_search_options(self, data, field_class):
        text = ""
        for x in data:
            if text == "":
                text = text + x[0] + ' = "' + x[1] + '"'
            else:
                text = text + ", " + x[0] + ' = "' + x[1] + '"'
        return field_class + "(" + text + ")"

    def clean_stack(self):
        self.facet_stack.reverse()
        del_indices = []
        del self.facet_stack[:1]
        for facet in self.facet_stack:
            if "props_num" in facet and facet["props_num"] == 1:
                del_indices.append(self.facet_stack.index(facet))
            elif "props_num" in facet:
                facet["props_num"] = facet["props_num"] - 1
                break
        for i in del_indices[::-1]:
            del self.facet_stack[i]
        self.facet_stack.reverse()

    def properties_types(self, data, array=False):
        count = 0
        ft = False
        if array:
            try:
                sch_type = self.get_type(data)
            except:
                sch_type = None
            if "type" in data and data["type"] == "nested":
                self.definition["nested"] = True
            elif sch_type and sch_type == "object":
                self.definition["obj"] = True
                data = data["properties"]
            elif "type" in data and data["type"] == "fulltext+keyword":
                self.definition["keyword"] = True
                self.definition["basic_array"] = True
                return 1
            elif "type" in data:
                fd = datatypes.get_datatype(
                    data, data.type, self.current_model, self.schema, self.stack
                )
                ft = fd.facet(key="")
                if ft:
                    self.definition["basic_array"] = True
                    return 1
            else:
                return 0
        for d in data:
            if "properties" in data[d]:
                count = count + 1
            elif "type" in data[d]:
                fd = datatypes.get_datatype(
                    data[d], data[d].type, self.current_model, self.schema, self.stack
                )
                ft = fd.facet(key=d)
                if ft:
                    count = count + 1
        return count

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

    def get_type(self, data):
        fd = datatypes.get_datatype(
            data, data.type, self.current_model, self.schema, self.stack
        )
        return fd.schema_type
