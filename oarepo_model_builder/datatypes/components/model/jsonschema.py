import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import PermissiveSchema

from .utils import set_default


class JSONSchema(ma.Schema):
    alias = ma.fields.Str(
        metadata={"doc": "Alias under which jsonschema is referenced in setup.cfg"}
    )
    version = ma.fields.Str(metadata={"doc": "Schema version"})
    name = ma.fields.Str(metadata={"doc": "Schema name"})
    file_ = ma.fields.Str(
        data_key="file", attribute="file", metadata={"doc": "Path to schema file"}
    )

    # json schema
    template = ma.fields.Nested(
        PermissiveSchema,
        metadata={"doc": "Template that will be merged with the schema"},
    )

    class Meta:
        unknown = ma.RAISE


class JSONSchemaModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        jsonschema = ma.fields.Nested(
            JSONSchema,
            data_key="json-schema",
            attribute="json-schema",
            metadata={
                "doc": "JSON Schema section of the model. Properties will be generated automatically"
            },
        )

    def before_model_prepare(self, datatype, **kwargs):
        extension_suffix = datatype.definition["extension-suffix"]
        records_path = datatype.definition["record-records-path"]

        json_schema = set_default(datatype, "json-schema", {})
        json_schema.setdefault("alias", extension_suffix)
        version = json_schema.setdefault(
            "version", datatype.schema.settings.get("version", "1.0.0")
        )

        schema_name = setdefault(
            json_schema,
            "name",
            f"{snake_case(model['record-prefix'])}-{version}.json",
        )

        json_schema.setdefault(
            "file",
            os.path.join(records_path, "jsonschemas", schema_name),
        )
