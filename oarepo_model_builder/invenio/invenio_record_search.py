from .invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.builders import process
from ..utils.hyphen_munch import HyphenMunch
from ..utils.schema import is_schema_element, match_schema, Ref
from ..outputs.json_stack import JSONStack
from oarepo_model_builder.utils.jinja import package_name

OAREPO_FACETS_PROPERTY = 'oarepo:facets'

class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_record_search'
    class_config = 'record-search-options-class'
    template = None

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.template = 'record-search-options'
        self.search_options_data = []
        self.search_facets_definiton = []
        self.search_options_stack = JSONStack()
        self.facets_definition = []
        self.facets_names = []


    def finish(self, **extra_kwargs):
        super().finish(
            search_options_data = self.search_options_data,
            facets_definition = self.facets_definition
        )
        python_path = self.class_to_path(self.settings.python['record-facets-class'])
        self.process_template(python_path, "record-facets",
                              current_package_name=package_name(self.settings.python['record-facets-class']),
                              search_options_data=self.search_options_data,
                              **extra_kwargs)

    @process('/model/**', condition=lambda current, stack: is_schema_element(stack))
    def enter_model_element(self):
        schema_path = match_schema(self.stack)
        if isinstance(schema_path[-1], Ref):
            schema_element_type = schema_path[-1].element_type
        else:
            schema_element_type = None

        definition = None
        recurse = True

        if recurse:
            # process children
            self.build_children()

        data = self.stack.top.data

        if not self.search_options_stack:
            return


        if schema_element_type == 'property' and data.type != "text" and data.type != "fulltext" and data.type != "object" and data.type != "nested":
            definition = data.get(OAREPO_FACETS_PROPERTY, {})
            nested_paths = []
            nested_path = ''
            nested = False
            path_stack = self.stack.stack[3:] #start inside model properties
            for upper in path_stack:
                if upper.key =='properties':
                    continue
                nested_path = nested_path + upper.key + '.'
                if upper.data.get("oarepo:mapping", HyphenMunch({'type': ''})).type == "nested":
                    nested_paths.append(nested_path)
            if len(nested_paths) > 0:
                nested = True

            name = self.process_name(self.stack.path, type = "name")
            if data.type== "fulltext+keyword":
                name = name + '_keyword'
            if name == "$schema":
                name = "_schema"
            if name == "id":
                name = "_id"
            class_string = ''

            if nested:
                class_string = 'NestedLabeledFacet('
                for path in nested_paths:
                    if nested_paths[-1] == path:
                        class_string = class_string + 'path = ' + '"' +  path[:-1] + '"'
                    else:
                        class_string = class_string + 'path = ' + '"' + path[:-1] + '"' + ', nested_facet = NestedLabeledFacet('

            if 'field' in definition:
                field = definition['field']
                if nested:
                    class_string = class_string + ' , nested_facet =' + field
                    for x in nested_paths:
                        class_string = class_string + ')'
                    self.search_options_data.append({name: class_string})
                else:
                    self.search_options_data.append({name: field})
            else:
                search_data = []
                field = self.process_name(self.stack.path, type = "field")
                if data.type == "fulltext+keyword":
                    field = field + '.keyword'
                search_data.append(['field', field])
                facets_class = definition.get('class', "TermsFacet")
                for key, value in definition.items():
                    if 'class' != key and 'field' != key:
                        search_data.append([key, value])
                if nested:
                    search_options = self.process_search_options(search_data, facets_class)
                    search_options = class_string + ' , nested_facet =' + search_options
                    for x in nested_paths:
                        search_options = search_options + ')'

                else:
                    search_options = self.process_search_options(search_data, facets_class)
                self.search_options_data.append({name: search_options})
            facets_name = "facets." + name
            self.facets_definition.append({name: facets_name})


    def process_search_options(self, data, field_class):
        text = ''
        for x in data:
            if text == "":
                text = text + x[0] + ' = "' + x[1]+ '"'
            else:
                text = text + ', ' + x[0] + ' = "'  + x[1] + '"'
        return field_class + '(' + text + ')'


    def process_name(self, path, type):
        path_array = (path.split('/'))[3:]
        name = path_array[0]
        if len(path_array) == 1:
            return name
        path_array.pop(0)

        for path in path_array:
            if path == "properties":
                continue
            if type == "name":
                name = name + '_' + path
            elif type == "field":
                name = name + '.' + path

        return name
