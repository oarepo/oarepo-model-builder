from collections import defaultdict
from typing import List

from oarepo_model_builder.datatypes import DataType, datatypes
from oarepo_model_builder.datatypes.components.marshmallow.graph import (
    collect_imports,
    set_package_dependencies,
    sort_by_reference_count,
)
from oarepo_model_builder.datatypes.components.marshmallow.object import (
    MarshmallowClass,
)
from oarepo_model_builder.utils.jinja import package_name

from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search"
    class_config = "record-search-options-class"
    template = "record-search-options"


    def build_node(self, node: DataType):
        # everything is done in finish
        pass

    def finish(self, **extra_kwargs):
        facets_list = self._generate_facets(self.current_model, **extra_kwargs) #todo FacetClass schema
        # classes.sort(
        #     key=lambda x: (
        #         "Metadata" in x.class_name,
        #         "Record" in x.class_name,
        #         x.class_name,
        #     )
        # )
        # classes_by_packages = defaultdict(list)
        # for cls in facets:
        #     classes_by_packages[package_name(cls.class_name)].append(cls)
        # for single_package_classes in classes_by_packages.values():
        #     sort_by_reference_count(single_package_classes)
        # if len(classes_by_packages.keys()) > 1:
        #     set_package_dependencies(classes_by_packages)
        #
        # for pn, single_package_classes in classes_by_packages.items():
        #     collect_imports(pn, single_package_classes)
        #     # generate and merge python source
        #     self.generate_package(pn, single_package_classes)
        # files were generated, so we are not calling super().finish() here

    def _generate_facets(self, node: DataType, **extra_kwargs):
        """
        validace sou v datatypes -done
        to co se deje v soucasnem je asi jedno, nebot ted se to beztak bude diti jinak
        co se deje v marshmallow:
            v invenio records marshmallow - ziska seznam marshmallow class, na nich neco udela a pak to zapise
            17:35
        """
        facets = []
        to_process = [node]

        # while to_process:
        #
        #     n = to_process.pop(0)
        #     # marshmallow_section = n.section_marshmallow
        #     datatypes.call_components(
        #             n,
        #             "build_facets",
        #             facets=facets,
        #     )
        #     print('jej')
        #     # to_process.extend(marshmallow_section.children.values())
        #     # if marshmallow_section.item:
        #     #     to_process.append(marshmallow_section.item)
        print(facets)
        # return facets
        python_path = self.class_to_path(self.current_model.record_facets_class)

        self.process_template(
            python_path,
            "record-facets",
            current_package_name=package_name(self.current_model.record_facets_class),
            search_options_data=self.search_options_data,
            imports=list(sorted(self.imports)),
            **extra_kwargs,
        )

    # def generate_package(self, package_name, package_classes: List[MarshmallowClass]):
    #     python_path = self.class_to_path(f"{package_name}.Dummy")
    #
    #     imports = [*self.extra_imports]
    #
    #     for cls in package_classes:
    #         imports.extend(cls.imports)
    #         for fld in cls.fields:
    #             imports.extend(fld.imports)
    #
    #     imports = list(sorted(set(imports), key=lambda x: (x.import_path, x.alias)))
    #
    #     self.process_template(
    #         python_path,
    #         self.template,
    #         current_package_name=package_name,
    #         imports=imports,
    #         generated_classes=package_classes,
    #     )


# from typing import Set
#
# from oarepo_model_builder.utils.jinja import package_name
#
# from ..datatypes import datatypes
# from ..datatypes.datatypes import MergedAttrDict
# from ..utils.deepmerge import deepmerge
# from .invenio_base import InvenioBaseClassPythonBuilder
#
# OAREPO_FACETS_PROPERTY = "facets"
# OAREPO_SORTABLE_PROPERTY = "sortable"
#
#
# class InvenioRecordSearchOptionsBuilder(InvenioBaseClassPythonBuilder):
#     TYPE = "invenio_record_search"
#     class_config = "record-search-options-class"
#     template = None
#
#     def begin(self, schema, settings):
#         super().begin(schema, settings)
#         self.template = "record-search-options"
#         self.search_options_data = []
#         self.sort_options_data = []
#         self.facets_definition = []
#         self.settings = settings
#         # if "sortable" in schema.schema:
#         #     self.process_top_sortable(schema.schema["sortable"])
#         self.facet_stack = []
#         self.imports = set()
#
#     def finish(self, **extra_kwargs):
#         return
#         super().finish(
#             search_options_data=self.search_options_data,
#             facets_definition=self.facets_definition,
#             sort_definition=self.sort_options_data,
#         )
#         python_path = self.class_to_path(self.current_model.record_facets_class)
#         section = getattr(
#             self.current_model,
#             f"section_mb_{self.TYPE.replace('-', '_')}",
#         )
#         merged = MergedAttrDict(section.config, self.current_model.definition)
#
#         self.process_template(
#             python_path,
#             "record-facets",
#             current_module=package_name(self.current_model.record_facets_class),
#             search_options_data=self.search_options_data,
#             imports=list(sorted(self.imports)),
#             vars=merged,
#             **extra_kwargs,
#         )
#
#     def process_top_sortable(self, data):
#         keys = dir(data)
#         for k in keys:
#             fields = dir(data[k])
#             fields_options = {}
#             for field in fields:
#                 fields_options = deepmerge(fields_options, {field: data[k][field]})
#             self.sort_options_data.append({k: fields_options})
#
#     # @process("**", condition=lambda current, stack: stack.schema_valid)
#     def enter_model_element(self):
#         schema_element_type = self.stack.top.schema_element_type
#         data = self.stack.top.data
#
#         self.build_children()
#
#         if schema_element_type == "property":
#             sort_definition = data.get(OAREPO_SORTABLE_PROPERTY, None)
#
#             if sort_definition != None:
#                 self.sort_options_data.append(
#                     self.process_sort_options(self.stack.path, sort_definition)
#                 )
#
#         facet_obj = get_facet_details(
#             stack=self.stack,
#             current_model=self.current_model,
#             schema=self.schema,
#             imports=self.imports,
#         )
#         for f in facet_obj:
#             facet = f["facet"]
#             path = f["path"]
#             self.search_options_data.append({path: facet})
#             search_ops_name = "facets." + path
#             self.facets_definition.append({path: search_ops_name})
#
#     def process_name(self, path, type):
#         path_array = (path.split("/"))[2:]
#         name = path_array[0]
#         if len(path_array) == 1:
#             return name
#         path_array.pop(0)
#         last_path = ""
#         for path in path_array:
#             if last_path != "properties" and path == "items":
#                 continue
#             last_path = path
#             if path == "properties":
#                 continue
#             if type == "name":
#                 name = name + "_" + path
#             elif type == "field":
#                 name = name + "." + path
#
#         return name
#
#     def process_sort_options(self, path, definition):
#         field = self.process_name(path=path, type="field")
#
#         key = definition.get("key", "")
#         if key == "":
#             key = self.process_name(path, "name")
#         order = definition.get("order", "asc")
#         if order == "desc":
#             field = "-" + field
#
#         return {key: dict(fields=[field])}
#
#
# def get_facet_details(stack, current_model, schema, imports: Set):
#     schema_element_type = stack.top.schema_element_type
#     data = stack.top.data
#
#     skip = True
#
#     if stack.top.schema_element_type in ["property", "items"]:
#         d_type = datatypes.get_datatype(
#             stack.top.data,
#             stack.top.key,
#             current_model,
#             schema,
#             stack,
#         )
#         for _imp in d_type.facet_imports:
#             import_path = _imp.get("import")
#             import_alias = _imp.get("alias")
#             if import_path:
#                 imports.add((import_path, import_alias))
#
#         if d_type.get_facet(None, ""):
#             stack_data = []
#             for s in stack.stack:
#                 type = s.schema_element_type
#                 if type and type == "property":
#                     stack_data.append(
#                         datatypes.get_datatype(
#                             s.data,
#                             s.key,
#                             current_model,
#                             schema,
#                             stack,
#                         )
#                     )
#                 elif type == "items":
#                     stack_data.append(
#                         datatypes.get_datatype(
#                             s.data,
#                             None,
#                             current_model,
#                             schema,
#                             stack,
#                         )
#                     )
#             skip = False
#
#             if current_model.get("searchable", True):
#                 for s in stack_data:
#                     if (
#                         "facets" in s.definition
#                         and "searchable" in s.definition["facets"]
#                         and not s.definition["facets"]["searchable"]
#                     ):
#                         skip = True
#                         break
#             else:
#                 skip = True
#                 for s in stack_data:
#                     if "facets" in s.definition:
#                         if (
#                             "searchable" in s.definition["facets"]
#                             and s.definition["facets"]["searchable"]
#                         ):
#                             skip = False
#                             break
#                         elif (
#                             "key" in s.definition["facets"]
#                             or "field" in s.definition["facets"]
#                         ):
#                             skip = False
#                             break
#     if skip:
#         return []
#
#     return datatypes.facet(stack_data)
