import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import convert_config_to_qualified_name
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .utils import set_default


class BlueprintSchema(ma.Schema):
    generate = ma.fields.Bool(metadata={"doc": "Generate blueprint, defaults to true"})
    alias = ma.fields.Str(
        metadata={
            "doc": "Alias under which the blueprint will be registered in the setup.cfg"
        }
    )
    extra_code = ma.fields.Str(metadata={"doc": "Extra code to be pasted to blueprint"})
    module = ma.fields.Str(metadata={"doc": "Module that will contain the blueprint"})
    function = ma.fields.Str(metadata={"doc": "Fully qualified blueprint function"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema),
        required=False,
        metadata={"doc": "Python imports"},
    )  # imports must be here as well as it is used on model's root (without field)

    class Meta:
        unknown = ma.RAISE


class BlueprintsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        ui_blueprint = ma.fields.Nested(
            BlueprintSchema,
            attribute="ui-blueprint",
            data_key="ui-blueprint",
            metadata={"doc": "UI blueprint details"},
        )
        api_blueprint = ma.fields.Nested(
            BlueprintSchema,
            attribute="api-blueprint",
            data_key="api-blueprint",
            metadata={"doc": "API blueprint details"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        alias = datatype.definition["module"]["alias"]
        module = datatype.definition["module"]["qualified"]
        profile = context["profile_module"]

        api = set_default(datatype, "api-blueprint", {})
        api.setdefault("generate", True)
        api.setdefault("alias", alias)
        api.setdefault("extra_code", "")
        api_module = api.setdefault(
            "module",
            f"{module}.views.{profile}.api",
        )
        api.setdefault(
            "function",
            f"{api_module}.create_blueprint_from_app",
        )
        api.setdefault("imports", [])
        convert_config_to_qualified_name(api, name_field="function")

        ui = set_default(datatype, "ui-blueprint", {})
        ui.setdefault("generate", True)
        ui.setdefault("alias", alias)
        ui.setdefault("extra_code", "")
        ui_module = ui.setdefault(
            "module",
            f"{module}.views.{profile}.ui",
        )
        ui.setdefault(
            "function",
            f"{ui_module}.create_blueprint_from_app",
        )
        ui.setdefault("imports", [])
        convert_config_to_qualified_name(ui, name_field="function")