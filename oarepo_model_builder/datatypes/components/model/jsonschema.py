import os

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import module_to_path, parent_module
from oarepo_model_builder.validation.utils import PermissiveSchema

from .defaults import DefaultsModelComponent
from .record import RecordModelComponent
from .utils import set_default


class JSONSchema(ma.Schema):
    generate = ma.fields.Bool(
        metadata={"doc": "Generate json schema (default is true)"}
    )
    alias = ma.fields.Str(
        metadata={"doc": "Alias under which jsonschema is referenced in setup.cfg"}
    )
    version = ma.fields.Str(metadata={"doc": "Schema version"})
    name = ma.fields.Str(metadata={"doc": "Schema name"})
    module = ma.fields.Str(metadata={"doc": "Schema module"})
    file_ = ma.fields.Str(
        data_key="file", attribute="file", metadata={"doc": "Path to schema file"}
    )

    # json schema
    template = ma.fields.Nested(
        PermissiveSchema,
        metadata={"doc": "Template that will be merged with the schema"},
    )
    skip = ma.fields.Boolean()

    class Meta:
        unknown = ma.RAISE


class JSONSchemaModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, RecordModelComponent]

    class ModelSchema(ma.Schema):
        jsonschema = ma.fields.Nested(
            JSONSchema,
            data_key="json-schema-settings",
            attribute="json-schema-settings",
            metadata={
                "doc": "JSON Schema section of the model. Properties will be generated automatically"
            },
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        prefix_snake = datatype.definition["module"]["prefix-snake"]
        alias = datatype.definition["module"]["alias"]
        records_path = module_to_path(
            parent_module(datatype.definition["record"]["module"])
        )

        json_schema = set_default(datatype, "json-schema-settings", {})
        json_schema.setdefault("generate", True)
        json_schema.setdefault("alias", alias)
        version = json_schema.setdefault(
            "version", datatype.schema.settings.get("version", "1.0.0")
        )
        json_schema.setdefault(
            "module",
            f'{parent_module(datatype.definition["record"]["module"])}.jsonschemas',
        )
        schema_name = json_schema.setdefault(
            "name",
            f"{prefix_snake}-{version}.json",
        )

        json_schema.setdefault(
            "file",
            os.path.join(records_path, "jsonschemas", schema_name),
        )
