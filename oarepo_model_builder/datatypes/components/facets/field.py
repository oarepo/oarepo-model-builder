import marshmallow as ma
from marshmallow import fields

from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.utils.facet_helpers import facet_name, flatten
from oarepo_model_builder.validation.utils import ImportSchema

from ...datatypes import DataTypeComponent
from . import FacetDefinition


class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    searchable = ma.fields.Bool(required=False)
    key = fields.String(required=False)
    field = fields.String(required=False)
    facet_class = fields.String(
        required=False, data_key="facet-class", attribute="facet-class"
    )
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

    def facet_path(self, datatype, facet_section):
        _path = datatype.path
        if "path" in facet_section:
            path = _path + "." + facet_section["path"]
        else:
            path = _path
        return path

    def process_facets(self, datatype, section, **__kwargs):
        # create the facet definition
        facet_section = section.config

        path = self.facet_path(datatype, facet_section)
        facet_definition = FacetDefinition(
            path=facet_section.get("key", facet_name(datatype.path)),
            dot_path=datatype.path,
            searchable=facet_section.get("searchable"),
            imports=facet_section.get("imports", []),
        )

        # set the field on the definition
        label = facet_section.get("label", f'{datatype.path.replace(".", "/")}.label')
        facet_definition.set_field(
            facet_section,
            arguments=[
                f"field={repr(path)}",
                f"label =_({repr(label)})",
                *facet_section.get("args", []),
            ],
        )

        # if there is indeed a facet here, process via parents
        if facet_definition.field:
            facets = flatten(
                datatypes.call_components(
                    datatype.parent,
                    "build_facet_definition",
                    facet_definition=facet_definition,
                )
            )
        else:
            facets = []

        # and store it on the element
        section.config["facets"] = facets
        return section
