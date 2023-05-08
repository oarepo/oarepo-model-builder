import os

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import module_to_path, parent_module
from oarepo_model_builder.validation.utils import PermissiveSchema

from .defaults import DefaultsModelComponent
from .jsonschema import JSONSchemaModelComponent
from .record import RecordModelComponent
from .utils import set_default


class ModelMappingSchema(ma.Schema):
    generate = ma.fields.Bool(metadata={"doc": "Generate mapping (default is true)"})
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
    depends_on = [
        DefaultsModelComponent,
        RecordModelComponent,
        JSONSchemaModelComponent,
    ]

    class ModelSchema(ma.Schema):
        mapping = ma.fields.Nested(
            ModelMappingSchema, metadata={"doc": "Mapping definition"}
        )

    def before_model_prepare(self, datatype, **kwargs):
        prefix_snake = datatype.definition["module"]["prefix-snake"]
        alias = datatype.definition["module"]["alias"]
        records_path = module_to_path(
            parent_module(datatype.definition["record"]["module"])
        )

        mapping = set_default(datatype, "mapping", {})
        mapping.setdefault("generate", True)
        mapping.setdefault("alias", alias)
        index_name = mapping.setdefault(
            "index", f"{prefix_snake}-{datatype.definition['json-schema']['version']}"
        )
        mapping.setdefault(
            "file",
            os.path.join(
                records_path,
                "mappings",
                "os-v2",
                index_name,
            ),
        )
