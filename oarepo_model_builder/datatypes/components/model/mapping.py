import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import PermissiveSchema

from .utils import set_default


class ModelMappingSchema(ma.Schema):
    alias = ma.fields.Str(
        metadata={
            "doc": "Index alias, under which the mapping is registered in setup.cfg"
        }
    )
    index = ma.fields.Str(metadata={"doc": "Index name"})
    file_ = ma.fields.Str(
        data_key="file", attribute="file", metadata={"doc": "Path to index file"}
    )

    # mapping
    template = ma.fields.Nested(
        PermissiveSchema,
        metadata={"doc": "Mapping template, merged with generated mapping"},
    )

    class Meta:
        unknown = ma.RAISE


class MappingModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        mapping = ma.fields.Nested(
            ModelMappingSchema, metadata={"doc": "Mapping definition"}
        )

    def before_model_prepare(self, datatype, **kwargs):
        extension_suffix = datatype.definition["extension-suffix"]
        records_path = datatype.definition["record-records-path"]

        mapping = set_default(datatype, "mapping", {})
        mapping.setdefault("alias", extension_suffix)
        index_name = mapping.setdefault("index", snake_case(model["record-prefix"]))
        mapping.setdefault(
            "file",
            lambda: os.path.join(
                records_path,
                "mappings",
                "os-v2",
                index_name,
            ),
        )
