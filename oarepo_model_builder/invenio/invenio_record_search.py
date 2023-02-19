from oarepo_model_builder.builders import process
from oarepo_model_builder.utils.jinja import package_name
from ..datatypes import datatypes

from ..outputs.json_stack import JSONStack
from ..utils.deepmerge import deepmerge
from ..utils.hyphen_munch import HyphenMunch
from .invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.python_name import convert_name_to_python

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
        self.search_facets_definiton = []
        self.search_options_stack = JSONStack()
        self.facets_definition = []
        self.facets_names = []
        self.settings = settings
        if "sortable" in schema.schema:
            self.process_top_sortable(schema.schema["sortable"])

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
                fd = datatypes.get_datatype(data, data.type, self.current_model, self.schema, self.stack)
                # fd.facet('g')
                ft = False
                if fd.schema_type == 'object':
                    properties = data.get('properties', {})
                    ft = fd.facet(key = self.stack.top.key, props_num= self.properties_types(properties))
                elif fd.schema_type == 'array':
                    ft = fd.facet(key = self.stack.top.key, props_num= self.properties_types(data['items'], True), definition=self.definition)

                if ft:
                    self.facet_stack.append(ft)
            except: pass
                # if not fd.facet('q'):
                #     pass
            # process children
            self.build_children()

        # data = self.stack.top.data

        if not self.search_options_stack:
            return

        if schema_element_type == "property":
            sort_definition = data.get(OAREPO_SORTABLE_PROPERTY, None)

            if sort_definition != None:
                self.sort_options_data.append(
                    self.process_sort_options(self.stack.path, sort_definition)
                )
        # array_items_type = None
        # if schema_element_type == "property" and data.type == "array":
        #     try:
        #         array_items_type = data["items"]["type"]
        #     except:
        #         array_items_type = None
        # print(data)
        if schema_element_type == "property" and \
                (('type' in data) and (datatypes.get_datatype(data, data.type, self.current_model, self.schema, self.stack).schema_type != 'object')):
                #todo check ze sem neleze obj array - array co ma v sobe obejkt, coz ale nejde detekovat pres count
                #mozna veskere kontejnery
            # and data.type != "text"
            # and data.type != "fulltext"
            # and data.type != "object"
            # and data.type != "nested"
            # and not (data.type == "array" and array_items_type == "fulltext")

            # definition = data.get(OAREPO_FACETS_PROPERTY, {})

            d_type = datatypes.get_datatype(data, data.type, self.current_model, self.schema, self.stack)
            ft = d_type.facet(key=self.stack.top.key, definition=self.definition)
            if ft and data.type != "array": self.facet_stack.append(ft)
            print(self.facet_stack)
            # todo smazat ten if
            if True and len(self.facet_stack) > 0:
                facet_def = ""
                facet_name = ""
                facet_path = ""
                nested_count = 0
                #todo prohnat nazvy tou metodou
                for facet in self.facet_stack:
                    facet_name = facet_name + convert_name_to_python(facet["path"]) + "_" #todo maybe in method
                    facet_path = facet_path + facet["path"] + "." #todo maybe in method
                    # if 'simple_array' in facet:
                    #     pass
                    if 'defined_class' in facet:
                        facet_def = facet_def + facet["class"]
                    elif facet['class'].startswith("Nested"):
                        nested_count += 1
                        facet_def = facet_def + f"NestedLabeledFacet(path =\" {facet_path[:-1]}\", nested_facet="
                    elif 'props_num' in facet:
                            # and facet['props_num'] is not None:

                        pass
                    # elif facet["class"].endswith(")"): #todo lip mozna? toto je z definice tak...
                    #     facet_def = facet_def + facet["class"]
                    else:
                        facet_path = (facet_path[::-1]).replace('_keyword.'[::-1], '.keyword.'[::-1], 1)[::-1] \
                            if facet_path.endswith('_keyword.') else facet_path
                        facet_def = facet_def + facet["class"] + f"\"{facet_path[:-1]}\""
                        for i in range(0, nested_count):
                            facet_def = facet_def + ')'
                        facet_def = facet_def + ')'
                self.clean_stack()
                # if facet_name == "$schema_":
                #     facet_name = "_schema_"
                # if facet_name == "id_":
                #     facet_name = "_id_"
                facet_name = facet_name[:-1]
                self.search_options_data.append({facet_name: facet_def})
                search_ops_name = "facets." + facet_name
                self.facets_definition.append({facet_name: search_ops_name})
            # else:
            #     nested_paths = []
            #     nested_path = ""
            #     nested = False
            #     path_stack = self.stack.stack[2:]  # start inside model properties
            #     for upper in path_stack:
            #         if upper.key == "properties":
            #             continue
            #         nested_path = nested_path + upper.key + "."
            #         if upper.data.get("mapping", {"type": ""}).get("type") == "nested":
            #             nested_paths.append(nested_path)
            #     if len(nested_paths) > 0:
            #         nested = True
            #
            #     # if "key" in definition:
            #     #     name = definition["key"]
            #     else:
            #         name = self.process_name(self.stack.path, type="name")
            #     # if data.type == "fulltext+keyword" and "key" not in definition:
            #     #     name = name + "_keyword"
            #     if name == "$schema":
            #         name = "_schema"
            #     if name == "id":
            #         name = "_id"
            #     class_string = ""
            #
            #     if nested:
            #         class_string = "NestedLabeledFacet("
            #         for path in nested_paths:
            #             if nested_paths[-1] == path:
            #                 class_string = class_string + "path = " + '"' + path[:-1] + '"'
            #             else:
            #                 class_string = (
            #                     class_string
            #                     + "path = "
            #                     + '"'
            #                     + path[:-1]
            #                     + '"'
            #                     + ", nested_facet = NestedLabeledFacet("
            #                 )

                # if "field" in definition:
                #     field = definition["field"]
                #     if nested:
                #         class_string = class_string + " , nested_facet =" + field
                #         for x in nested_paths:
                #             class_string = class_string + ")"
                #         self.search_options_data.append({name: class_string})
                #     else:
                #         self.search_options_data.append({name: field})
                # else:
                #     search_data = []
                #     field = self.process_name(self.stack.path, type="field")
                #     if data.type == "fulltext+keyword":
                #         field = field + ".keyword"
                #     search_data.append(["field", field])
                #     facets_class = definition.get("class", "TermsFacet")
                #     for key, value in definition.items():
                #         if "class" != key and "field" != key:
                #             search_data.append([key, value])
                #     if nested:
                #         search_options = self.process_search_options(
                #             search_data, facets_class
                #         )
                #         search_options = class_string + " , nested_facet =" + search_options
                #         for x in nested_paths:
                #             search_options = search_options + ")"
                #
                #     else:
                #         search_options = self.process_search_options(
                #         search_data, facets_class
                #         )
                #     self.search_options_data.append({name: search_options})
                # facets_name = "facets." + name
                # self.facets_definition.append({name: facets_name})

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
            if 'props_num' in facet and facet['props_num'] == 1:
                del_indices.append(self.facet_stack.index(facet))
            elif 'props_num' in facet:
                facet['props_num'] = facet['props_num'] -1

                break

        for i in del_indices[::-1]:
            del self.facet_stack[i]
        self.facet_stack.reverse()

    # def refactor_name(self, facet_name, facet_path = False):
    #     facet_name = facet_name.replace('@', "_") #for relation field purposes
    #     if not facet_path:
    #         if facet_name == 'id': facet_name = "_id" #special case
    #         if not facet_name[0].isalpha() and facet_name[0] != "_":
    #             facet_name = facet_name[1:]
    #             facet_name = "_" + facet_name
    #
    #     return  facet_name


    def properties_types(self, data, array = False):#todo check
        count = 0
        #todo add this to facet method?
        if array:
            if 'type' in data and data['type'] == 'object': #todo  1: check if facetable
                self.definition['obj'] = True
                data = data['properties']
                print(data)
            elif 'type' in data and data['type'] == 'nested':
                self.definition['nested'] = True
            elif 'type' in data and data['type'] == "fulltext+keyword":
                self.definition['keyword'] = True
                return 1
            elif 'type' in data and data['type'] != "text" and data['type'] != "fulltext":
                # self.definition['simple_array'] = True
                return 1
            else:
                return 0
        for d in data:
            if 'properties' in data[d]:
                count = count + 1
            elif 'type' in data[d] and data[d].type != "text" and data[d].type != "fulltext": #todo pomoci facet spis nejak hm
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
