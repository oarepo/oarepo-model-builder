from .invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.builders import process
from oarepo_model_builder.stack import ModelBuilderStack
from ..utils.schema import is_schema_element, match_schema, Ref
from ..outputs.json_stack import JSONStack
from deepmerge import always_merger
from oarepo_model_builder.utils.jinja import package_name

OAREPO_FACETS_PROPERTY = 'oarepo:facets'

class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_record_search'
    class_config = 'record-search-options-class'
    template = 'record-search-options'
    search_options_data = []
    facets_definition = []

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.search_options_stack = JSONStack()


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
    def enter_model_element(self, stack: ModelBuilderStack):
        schema_path = match_schema(stack)
        if isinstance(schema_path[-1], Ref):
            schema_element_type = schema_path[-1].element_type
        else:
            schema_element_type = None

        definition = None
        recurse = True

        if recurse:
            # process children
            yield
        else:
            # skip children
            yield stack.SKIP
        data = stack.top.data

        if not self.search_options_stack:
            return
        if schema_element_type == 'property' and data.type != "text" and data.type != "object" and data.type != "nested":
            definition = data.get(OAREPO_FACETS_PROPERTY, {})
            print('path', stack.path)
            name = self.process_name(stack.path, type = "name")

            if data.type== "fulltext+keyword":
                name = name + '_keyword'
            if name == "$schema":
                name = "_schema"
            if name == "id":
                name = "_id"

            if 'field' in definition:
                field = definition['field']
                self.search_options_data.append({name: field})
                # always_merger.merge(self.search_options_data, {name: field})
            else:
                search_data = []
                field = self.process_name(stack.path, type = "field")
                search_data.append(['field', field])
                facets_class = definition.get('class', "TermsFacet")
                for key, value in definition.items():
                    if 'class' != key and 'field' != key:
                        search_data.append([key, value])
                search_options = self.process_search_options(search_data, facets_class)
                self.search_options_data.append({name: search_options})
            facets_name = "facets." + name
            self.facets_definition.append({name: facets_name})
                # always_merger.merge(self.search_options_data, {name: search_options})



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
