import re

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import parent_module
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .record import RecordModelComponent
from .utils import set_default


class PIDSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Set to True (default) provider class"})
    pid_type = ma.fields.String(
        attribute="type",
        data_key="type",
        metadata={"doc": "PID type, generated from model name if not passed"},
    )
    provider_class = ma.fields.String(
        attribute="provider-class",
        data_key="provider-class",
        metadata={"doc": "Fully qualified name of the provider class"},
    )
    provider_base_classes = ma.fields.List(
        ma.fields.String(),
        attribute="provider-base-classes",
        data_key="provider-base-classes",
        metadata={"doc": "List of provider base classes"},
    )
    field_class = ma.fields.String(
        attribute="field-class",
        data_key="field-class",
        metadata={"doc": "Field class, PIDField is used if not passed in"},
    )
    context_class = ma.fields.String(
        attribute="context-class",
        data_key="context-class",
        metadata={"doc": "Context class, PIDFieldContext is used if not passed"},
    )

    field_args = ma.fields.List(
        ma.fields.String(),
        attribute="field-args",
        data_key="field-args",
        metadata={"doc": "Field arguments, default is create=True"},
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "A list of python imports"}
    )
    module = ma.fields.String(
        metadata={"doc": "Module where the pid provider will be placed"}
    )
    skip = ma.fields.Boolean()


class PIDModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, RecordModelComponent]

    class ModelSchema(ma.Schema):
        pid = ma.fields.Nested(PIDSchema, metadata={"doc": "PID settings"})

    def before_model_prepare(self, datatype, *, context, **kwargs):
        prefix = datatype.definition["module"]["prefix"]
        record_module = parent_module(datatype.definition["record"]["module"])

        pid = set_default(datatype, "pid", {})
        pid.setdefault("generate", True)
        pid.setdefault("type", process_pid_type(datatype.definition["model-name"]))

        pid_module = pid.setdefault(
            "module",
            f"{record_module}.api",
        )
        pid.setdefault(
            "provider-class",
            f"{pid_module}.{prefix}IdProvider",
        )
        pid.setdefault("provider-base-classes", ["RecordIdProviderV2"])

        pid.setdefault("field-class", "PIDField")
        pid.setdefault("context-class", "PIDFieldContext")
        pid.setdefault("field-args", ["create=True"])
        pid.setdefault(
            "imports",
            [
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDField"
                },
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
                },
                {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
            ],
        )


def process_pid_type(pid_base):
    pid_base = re.sub(r"[\s_-]", "", pid_base).lower()
    if len(pid_base) > 6:
        pid_base = re.sub(r"[AEIOU]", "", pid_base, flags=re.IGNORECASE)
    if len(pid_base) > 6:
        pid_base = pid_base[:3] + pid_base[len(pid_base) - 3 :]
    return pid_base
