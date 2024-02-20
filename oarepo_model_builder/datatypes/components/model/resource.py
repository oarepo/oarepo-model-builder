import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import convert_config_to_qualified_name
from oarepo_model_builder.validation.utils import ImportSchema

from .defaults import DefaultsModelComponent
from .utils import set_default


class ResourceClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Generate the resource class (default)"})
    config_key = ma.fields.Str(
        metadata={
            "doc": "Name of the config entry that holds the current resource class name"
        }
    )
    proxy = ma.fields.Str(
        metadata={"doc": "name of the generated proxy, will be put to _proxies_ module"}
    )
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the resource class"},
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
        metadata={"doc": "Extra code to be put to the bottom of the generated file"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    additional_args = ma.fields.List(
        ma.fields.String(),
        attribute="additional-args",
        data_key="additional-args",
        metadata={
            "doc": "List of additional arguments that will be passed to the resource constructor"
        },
    )
    skip = ma.fields.Boolean()


class ResourceConfigClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    base_url = ma.fields.String(
        data_key="base-url",
        attribute="base-url",
        metadata={"doc": "The base url of the resource"},
    )

    base_html_url = ma.fields.String(
        data_key="base-html-url",
        attribute="base-html-url",
        metadata={"doc": "The base html url of the resource"},
    )

    generate = ma.fields.Bool(
        metadata={"doc": "Generate the resource config class (default)"}
    )
    config_key = ma.fields.Str(
        metadata={
            "doc": "Name of the config entry that holds the current resource class name"
        }
    )
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the config class"},
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
        metadata={"doc": "Extra code to be put below the generated config class"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    additional_args = ma.fields.List(
        ma.fields.String(),
        attribute="additional-args",
        data_key="additional-args",
        metadata={
            "doc": "List of additional arguments that will be passed to the resource config constructor"
        },
    )
    skip = ma.fields.Boolean()


class ResourceModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        resource = ma.fields.Nested(
            ResourceClassSchema, metadata={"doc": "Resource class settings"}
        )
        resource_config = ma.fields.Nested(
            ResourceConfigClassSchema,
            attribute="resource-config",
            data_key="resource-config",
            metadata={"doc": "Resource config class settings"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        module_container = datatype.definition["module"]
        profile_package = context["profile_module"]

        resource_package = (
            f"{module_container['qualified']}.resources.{profile_package}"
        )

        resource = set_default(datatype, "resource", {})
        resource.setdefault("generate", True)
        resource.setdefault(
            "config-key",
            f"{module_container['base-upper']}_{context['profile_upper']}_RESOURCE_CLASS",
        )
        resource_module = resource.setdefault("module", f"{resource_package}.resource")
        resource.setdefault(
            "class",
            f"{resource_module}.{module_container['prefix']}Resource",
        )
        resource.setdefault(
            "proxy",
            "current_resource",
        )
        resource.setdefault("extra-code", "")
        resource.setdefault(
            "base-classes", ["invenio_records_resources.resources.RecordResource"]
        )
        resource.setdefault(
            "imports",
            [],
        )
        resource.setdefault("additional-args", [])
        convert_config_to_qualified_name(resource)

        config = set_default(datatype, "resource-config", {})
        config.setdefault("generate", True)
        config.setdefault("base-url", f"/{module_container['kebab-module']}/")
        config.setdefault("base-html-url", f"/{module_container['kebab-module']}/")
        config.setdefault(
            "config-key",
            f"{module_container['base-upper']}_{context['profile_upper']}_RESOURCE_CONFIG",
        )
        config_module = config.setdefault("module", f"{resource_package}.config")
        config.setdefault(
            "class",
            f"{config_module}.{module_container['prefix']}ResourceConfig",
        )
        config.setdefault("extra-code", "")

        config.setdefault(
            "base-classes", ["invenio_records_resources.resources.RecordResourceConfig"]
        )
        config.setdefault(
            "imports",
            [],
        )
        config.setdefault("additional-args", [])
        convert_config_to_qualified_name(config)
