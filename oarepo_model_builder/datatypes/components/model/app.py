import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import convert_config_to_qualified_name
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .utils import set_default


class ConfigSchema(ma.Schema):
    module = ma.fields.Str(metadata={"doc": "Module with app config"})
    extra_code = ma.fields.Str(
        metadata={"doc": "Extra code that will be pasted to app config"}
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema),
        required=False,
        metadata={"doc": "Python imports"},
    )  # imports must be here as well as it is used on model's root (without field)

    class Meta:
        unknown = ma.RAISE


class ExtSchema(ma.Schema):
    alias = ma.fields.Str(
        metadata={
            "doc": "Alias under which the extension will be registered in setup.cfg and in app.extensions"
        }
    )
    module = ma.fields.Str(metadata={"doc": "Module with ext schema"})
    class_ = ma.fields.Str(
        attribute="class", data_key="class", metadata={"doc": "Extension class name"}
    )
    base_classes = ma.fields.Str(
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "A list of extension's base classes"},
    )
    skip = ma.fields.Boolean()
    extra_code = ma.fields.Str(
        metadata={"doc": "Extra code that will be pasted to app extension module"}
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema),
        required=False,
        metadata={"doc": "Python imports"},
    )  # imports must be here as well as it is used on model's root (without field)

    class Meta:
        unknown = ma.RAISE


class AppModelComponent(DataTypeComponent):
    "flask application"
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        config = ma.fields.Nested(
            ConfigSchema, metadata={"doc": "Application config details"}
        )
        ext = ma.fields.Nested(
            ExtSchema, metadata={"doc": "Application extension details"}
        )

    def before_model_prepare(self, datatype, **kwargs):
        module = datatype.definition["module"]["qualified"]
        base_title = datatype.definition["module"]["base-title"]

        config = set_default(datatype, "config", {})

        config.setdefault("generate", True)
        config.setdefault("module", f"{module}.config")
        config.setdefault("extra_code", "")
        config.setdefault("imports", [])

        ext = set_default(datatype, "ext", {})

        ext.setdefault("generate", True)
        ext_module = ext.setdefault("module", f"{module}.ext")
        ext.setdefault("class", f"{ext_module}.{base_title}Ext")
        ext.setdefault("base-classes", [])
        ext.setdefault("extra_code", "")
        ext.setdefault("alias", module)
        ext.setdefault("imports", [])
        convert_config_to_qualified_name(ext)
