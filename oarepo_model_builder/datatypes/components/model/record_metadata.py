import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import parent_module
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .record import RecordModelComponent
from .utils import set_default


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
    alembic = ma.fields.Str(metadata={"doc": "module where alembic files are stored"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    skip = ma.fields.Boolean()


class RecordMetadataModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, RecordModelComponent]

    class ModelSchema(ma.Schema):
        record_metadata = ma.fields.Nested(
            RecordMetadataClassSchema,
            attribute="record-metadata",
            data_key="record-metadata",
            metadata={"doc": "Record metadata settings"},
        )

    def before_model_prepare(self, datatype, **kwargs):
        records_module = parent_module(datatype.definition["record"]["module"])
        prefix = datatype.definition["module"]["prefix"]
        alias = datatype.definition["module"]["alias"]

        metadata = set_default(datatype, "record-metadata", {})
        metadata.setdefault("generate", True)
        metadata_module = metadata.setdefault("module", f"{records_module}.models")
        metadata.setdefault("class", f"{metadata_module}.{prefix}Metadata")
        metadata.setdefault("base-classes", ["db.Model", "RecordMetadataBase"])
        metadata.setdefault("extra-code", "")
        metadata.setdefault(
            "imports",
            [
                {"import": "invenio_records.models.RecordMetadataBase"},
                {"import": "invenio_db.db"},
            ],
        )
        metadata.setdefault("table", f"{prefix.lower()}_metadata")
        metadata.setdefault("alembic", f"{records_module}.alembic")
        metadata.setdefault("alias", alias)
