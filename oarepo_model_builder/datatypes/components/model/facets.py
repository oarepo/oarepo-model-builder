import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType, datatypes
from oarepo_model_builder.datatypes.components.model.utils import set_default

from .defaults import DefaultsModelComponent


class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    searchable = ma.fields.Bool(required=False)

    extra_code = ma.fields.String(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be pasted to search options module"},
    )
    module = ma.fields.String(
        metadata={"doc": "Module where the facets will be placed"}
    )
    generate = ma.fields.Boolean()
    skip = ma.fields.Boolean()


class FacetsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        facets = ma.fields.Nested(
            FacetsSchema,
            required=False,
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        module = datatype.definition["module"]["qualified"]
        profile_module = context["profile_module"]

        facets = set_default(datatype, "facets", {})
        facets.setdefault("generate", True)
        facets.setdefault("module", f"{module}.services.{profile_module}.facets")

        facets.setdefault("extra-code", "")

    def process_facets(self, datatype, section, **kwargs):
        facets = []
        searchable = datatype.definition.get("searchable", True)
        datatypes.call_components(
            datatype,
            "build_facets",
            facets=facets,
            facet_definition=None,
            searchable=searchable,
        )
        section.config["facets"] = facets
        datatype.definition["config"]["facets"] = facets
        return section

    def build_facets(self, datatype, facets, facet_definition=None, searchable=True):
        for c in datatype.children.values():
            if c.model_type == "array":
                children = c.item.children
            else:
                children = c.children
            if children != {}:
                self.get_leaf(children, facets, searchable)
            else:
                datatypes.call_components(
                    c,
                    "build_facets",
                    facets=facets,
                    facet_definition=None,
                    searchable=searchable,
                )

        return facets

    def get_leaf(self, children, facets, searchable):
        for c in children.values():
            if c.model_type == "array":
                children = c.item.children
            else:
                children = c.children
            if children != {}:
                self.get_leaf(children, facets, searchable)
            else:
                datatypes.call_components(
                    c,
                    "build_facets",
                    facets=facets,
                    facet_definition=None,
                    searchable=searchable,
                )

    def build_definition(
        self, datatype, facets, facet_definition=None, searchable=True
    ):
        if facet_definition:
            facet_searchable = facet_definition.get("facet_searchable", searchable)
            if facet_searchable:
                facets.append(facet_definition)
