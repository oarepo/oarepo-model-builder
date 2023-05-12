import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.utils.python_name import (
    convert_config_to_qualified_name,
    parent_module,
)
from oarepo_model_builder.validation.utils import ImportSchema

from ..facets import RegularFacetsComponent
from .service import ServiceModelComponent
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
    skip = ma.fields.Boolean()
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class FacetsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE


class FacetsModelComponent(RegularFacetsComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ServiceModelComponent]

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
        service_module = parent_module(datatype.definition["service"]["module"])
        prefix = datatype.definition["module"]["prefix"]

        facets = set_default(datatype, "facets", {})
        facets.setdefault("module", f"{service_module}.facets")
        facets.setdefault("generate", True)
        facets.setdefault("extra-code", "")
        facets.setdefault("imports", [])

        search_options = set_default(datatype, "search-options", {})
        search_module = search_options.setdefault("module", f"{service_module}.search")
        search_options.setdefault("class", f"{search_module}.{prefix}SearchOptions")
        search_options.setdefault("base-classes", ["InvenioSearchOptions"])
        search_options.setdefault("generate", True)
        search_options.setdefault("extra-code", "")
        search_options.setdefault(
            "imports",
            [
                {
                    "import": "invenio_records_resources.services.SearchOptions",
                    "alias": "InvenioSearchOptions",
                }
            ],
        )
        convert_config_to_qualified_name(search_options)
