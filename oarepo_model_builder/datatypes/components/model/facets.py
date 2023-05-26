import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ..facets import FacetDefinition
from ..facets.object import ObjectFacetsComponent
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


class FacetsModelComponent(ObjectFacetsComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        facets = ma.fields.Nested(
            FacetsSchema,
            required=False,
        )

    def before_model_prepare(self, datatype, *, context, **__kwargs):
        module = datatype.definition["module"]["qualified"]
        profile_module = context["profile_module"]

        facets = set_default(datatype, "facets", {})
        facets.setdefault("generate", True)
        facets.setdefault("module", f"{module}.services.{profile_module}.facets")

        facets.setdefault("extra-code", "")

    def build_facet_definition(
        self,
        datatype,
        facet_definition: FacetDefinition,
    ):
        if facet_definition.searchable is None:
            facet_definition.searchable = datatype.definition.get("searchable", True)
        if facet_definition.searchable is not False:
            return [facet_definition]
        else:
            # facet will not be generated
            return []
