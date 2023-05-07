import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.validation.utils import ImportSchema

from ..facets import RegularFacetsComponent
from .utils import set_default


class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Set true (default) to generate facets"})

    extra_code = ma.fields.String(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code that will be copied to facet's file"},
    )
    module = ma.fields.String(
        metadata={"doc": "Module where the facets will be placed"}
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class SearchOptionsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(
        metadata={"doc": "Set true (default) to generate search options"}
    )

    extra_code = ma.fields.String(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be pasted to search options module"},
    )
    module = ma.fields.String(
        metadata={"doc": "Module where the facets will be placed"}
    )
    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of search options class"},
    )
    base_classes = ma.fields.String(
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "List of base classes"},
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE


class FacetsModelComponent(RegularFacetsComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        class Meta:
            unknown = ma.RAISE

    searchable = ma.fields.Bool()
    facets = ma.fields.Nested(
        FacetsSchema, metadata={"doc": "Definition of facet generator options"}
    )
    search_options = ma.fields.Nested(
        SearchOptionsSchema,
        attribute="search-options",
        data_key="search-options",
        metadata={"doc": "Definition of search options"},
    )

    def before_model_prepare(self, datatype, **kwargs):
        service_module = datatype.definition["record-services-module"]
        record_prefix = datatype.definition["record-prefix"]

        facets = set_default(datatype, "facets", {})
        facets.setdefault("module", f"{model['record-services-module']}.facets")
        facets.setdefault("generate", True)
        facets.setdefault("extra-code", "")

        search_options = set_default(datatype, "search-options", {})

        facets.setdefault(
            "class", f"{services_module}.search.{record_prefix}SearchOptions"
        )
        facets.setdefault("base-classes", [])
        facets.setdefault("generate", True)
        facets.setdefault("extra-code", "")
