import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.utils.facet_helpers import facet_name
from oarepo_model_builder.validation.utils import ImportSchema

from ...datatypes import DataTypeComponent


class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    searchable = ma.fields.Bool(required=False)
    key = fields.String(required=False)
    field = fields.String(required=False)
    facet_class = fields.String(required=False, data_key="facet-class")
    args = fields.List(fields.String(), required=False)
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    path = fields.String(required=False)
    keyword = fields.String(required=False)


class RegularFacetsComponent(DataTypeComponent):
    eligible_datatypes = []

    class ModelSchema(ma.Schema):
        facets = ma.fields.Nested(
            FacetsSchema,
            required=False,
        )

    def build_facets(self, datatype, facets, facet_definition=None, searchable=True):
        facet_section = datatype.section_facets
        if not facet_section.config == {}:
            _path = datatype.path
            if "keyword" in datatype.section_facets.config:
                _path = _path + ".keyword"
            if "path" in facet_section.config:
                path = _path + "." + facet_section.config["path"]

            else:
                path = _path
            key = facet_section.config.get("key", facet_name(_path))
            label = facet_section.config.get(
                "label", f'{_path.replace(".", "/")}.label'
            )
            facet_searchable = facet_section.config.get("searchable", searchable)
            imports = facet_section.config.get("imports", [])
            arguments = facet_section.config.get("args", [])
            arguments_string = ",".join(arguments)
            if arguments_string != "":
                arguments_string = "," + arguments_string
            field = facet_section.config.get(
                "field",
                datatype.section_facets.config["facet_class"]
                + f'(field="{path}", label =_("{label}") {arguments_string} '
                + ")",
            )
            facet_definition = {
                "path": key,
                "class": field,
                "facet_searchable": facet_searchable,
                "imports": imports,
            }
        datatypes.call_components(
            datatype.parent,
            "build_definition",
            facets=facets,
            facet_definition=facet_definition,
            searchable=searchable,
        )

    def create_definition(self, config, datatype):
        return {
            datatype.path: config["facet_class"] + f'(field="{datatype.path}"' + ")"
        }
