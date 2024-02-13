import marshmallow as ma

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.utils.python_name import parent_module
from oarepo_model_builder.validation.extensibility import ExtensibleSchema
from oarepo_model_builder.validation.utils import ImportSchema

from ..ui import ObjectUIComponent, ObjectUIExtraSchema
from .marshmallow import ModelMarshmallowSchema
from .resource import ResourceModelComponent
from .utils import set_default


class JSONSerializerSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    module = ma.fields.String(
        metadata={"doc": "UI serializer class module"},
    )
    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
        metadata={"doc": "UI serializer class qualified name"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "List of base classes"},
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
        metadata={
            "doc": "Extra code to be put below the generated ui serializer class"
        },
    )
    list_schema_cls = ma.fields.Str(
        attribute="list-schema-cls",
        data_key="list-schema-cls",
        metadata={"doc": "Marshmallow class for list serialization"},
    )
    format_serializer_cls = ma.fields.Str(
        attribute="format-serializer-cls",
        data_key="format-serializer-cls",
        metadata={"doc": "Class for serializing the resulting json"},
    )
    schema_context_args = ma.fields.Dict(
        attribute="schema-context-args",
        data_key="schema-context-args",
        metadata={"doc": "Extra args for ui marshmallow schema context"},
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    skip = ma.fields.Boolean()
    generate = ma.fields.Boolean()


class ModelUISchema(ObjectUIExtraSchema):
    marshmallow = ma.fields.Nested(ModelMarshmallowSchema)


class UIModelComponent(ObjectUIComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ResourceModelComponent]

    class ModelSchema(ma.Schema):
        ui = ma.fields.Nested(
            ExtensibleSchema("ui.model", ModelUISchema), metadata={"doc": "UI settings"}
        )
        json_serializer = ma.fields.Nested(
            JSONSerializerSchema,
            attribute="json-serializer",
            data_key="json-serializer",
        )

    def before_model_prepare(self, datatype, **kwargs):
        prefix = datatype.definition["module"]["prefix"]
        resources_module = parent_module(datatype.definition["resource"]["module"])

        set_default(datatype, "ui", {})

        json = set_default(datatype, "json-serializer", {})
        json_module = json.setdefault("module", f"{resources_module}.ui")
        json.setdefault("class", f"{json_module}.{prefix}UIJSONSerializer")
        json.setdefault(
            "base-classes", ["oarepo_runtime.resources.LocalizedUIJSONSerializer"]
        )
        json.setdefault(
            "imports",
            [],
        )
        json.setdefault("extra-code", "")
        json.setdefault("generate", True)
        json.setdefault("list_schema_cls", "flask_resources.BaseListSchema")
        json.setdefault(
            "format_serializer_cls", "flask_resources.serializers.JSONSerializer"
        )
        json.setdefault(
            "schema-context-args",
            {'"object_key"': '"ui"', '"identity"': "{{ flask.g{g.identity} }}"},
        )
