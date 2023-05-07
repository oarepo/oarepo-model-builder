import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import ImportSchema


class RecordMetadataClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    alias = ma.fields.Str(
        metadata={"doc": "Alias under which the metadata is registered in setup.cfg"}
    )
    generate = ma.fields.Bool(metadata={"doc": "True to generate the metadata class"})
    module = ma.fields.String(
        metadata={"doc": "Module where the metadata class resides"}
    )
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the class"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "A list of base classes"},
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be put below the record"},
    )
    table = ma.fields.Str(
        attribute="table",
        data_key="table",
        metadata={"doc": "Name of the database table"},
    )
    alembic = ma.fields.Str(metadata={"doc": "Name of the alembic branch"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class RecordMetadataModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        record_metadata = ma.fields.Nested(
            RecordMetadataClassSchema,
            attribute="record-metadata",
            data_key="record-metadata",
            metadata={"doc": "Record metadata settings"},
        )

    def before_model_prepare(self, datatype, **kwargs):
        module = datatype.definition["module"]
        profile_module = datatype.definition["profile-module"]
        record_prefix = datatype.definition["record-prefix"]

        metadata = setdefault(datatype, "record-metadata", {})
        metadata.setdefault("generate", True)
        records_module = metadata.setdefault("module", f"{module}.{profile_module}")
        metadata.setdefault("class", f"{records_module}.models.{record_prefix}Metadata")
        metadata.setdefault(
            "base-classes", ["invenio_records.models.RecordMetadataBase"]
        )
        metadata.setdefault("extra-code", "")
        metadata.setdefault("table", f"{record_prefix.lower()}_metadata")
        metadata.setdefault("alembic", f"{extension_suffix}")
        metadata.setdefault("alias", f"{extension_suffix}")
