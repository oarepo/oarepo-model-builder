import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent


class RecordSearchOptionsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

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
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the class"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "Model base classes"},
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )

    sort_options_field = ma.fields.Str(
        attribute="sort-options-field",
        data_key="sort-options-field",
    )

    fields = ma.fields.Dict(
        keys=ma.fields.Str(),
        values=ma.fields.Str(),
        metadata={"doc": "Fields to be used in search options"},
    )


class SearchOptionsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        search_options = ma.fields.Nested(
            RecordSearchOptionsSchema,
            required=False,
            data_key="search-options",
            attribute="search-options",
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        module = datatype.definition["module"]["qualified"]
        profile_module = context["profile_module"]
        record_search_prefix = datatype.definition["module"]["prefix"]

        record_search_options = set_default(datatype, "search-options", {})
        record_search_options.setdefault("generate", True)
        module = record_search_options.setdefault(
            "module", f"{module}.services.{profile_module}.search"
        )

        record_search_options.setdefault("extra-code", "")
        record_search_options.setdefault(
            "class", f"{module}.{record_search_prefix}SearchOptions"
        )
        record_search_options.setdefault(
            "base-classes",
            ["invenio_records_resources.services.SearchOptions{InvenioSearchOptions}"],
        )
        record_search_options.setdefault(
            "imports",
            [],
        )
        record_search_options.setdefault(
            "fields",
            {},
        )
        record_search_options.setdefault("sort-options-field", "sort_options")
