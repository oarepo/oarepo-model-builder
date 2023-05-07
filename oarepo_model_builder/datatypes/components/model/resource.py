import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.validation.utils import ImportSchema

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
    proxy = ma.fields.Str(metadata={"doc": "Qualified name of the generated proxy"})
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


class ResourceConfigClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    base_url = ma.fields.String(
        data_key="base-url",
        attribute="base-url",
        metadata={"doc": "The base url of the resource"},
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


class ResourceModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

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

    def before_model_prepare(self, datatype, **kwargs):
        module_container = datatype.definition["module"]

        resource_module = (
            f"{module_container['module']}.resources.{datatype.definition['profile']}"
        )

        resource = set_default(datatype, "resource", {})
        resource.setdefault("generate", True)
        resource.setdefault(
            "config-key",
            f"{module_container['base-upper']}_RESOURCE_CLASS_{module_container['suffix-upper']}",
        )
        resource.setdefault(
            "class",
            f"{resource_module}.{module_container['prefix']}Resource",
        )
        resource.setdefault(
            "proxy",
            f"{module_container['module']}.proxies.current_resource",
        )
        resource.setdefault(
            "proxy",
            f"{module_container['module']}.proxies.current_resource",
        )
        resource.setdefault("extra-code", "")
        resource.setdefault(
            "base-classes", ["invenio_records_resources.resources.RecordResource"]
        )

        config = set_default("datatype", "resource-config", {})
        config.setdefault("generate", True)
        config.setdefault("base-url", f"/{module_container['kebap-module']}/")
        config.setdefault(
            "config-key",
            f"{module_container['base-upper']}_RESOURCE_CONFIG_{module_container['suffix-upper']}",
        )
        config.setdefault(
            "class",
            f"{resource_module}.{module_container['prefix']}ResourceConfig",
        )
        config.setdefault(
            "proxy",
            f"{module_container['module']}.proxies.current_resource",
        )
        config.setdefault("extra-code", "")

        resource.setdefault(
            "base-classes", ["invenio_records_resources.resources.RecordResourceConfig"]
        )
