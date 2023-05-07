import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import convert_config_to_qualified_name
from oarepo_model_builder.validation.utils import ImportSchema

from .app import AppModelComponent
from .defaults import DefaultsModelComponent
from .utils import set_default


class ServiceClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Generate service class (default)"})
    config_key = ma.fields.Str(
        metadata={"doc": "Key under which actual service class is registered in config"}
    )
    proxy = ma.fields.Str(metadata={"doc": "name of the service proxy, will be put to _proxies_ package"})
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the service class"},
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
        metadata={"doc": "Extra code to be put below the generated service class"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class ServiceConfigClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    service_id = ma.fields.String(
        attribute="service-id",
        data_key="service-id",
        metadata={"doc": "ID of the service"},
    )
    generate = ma.fields.Bool(metadata={"doc": "Generate the service config"})
    config_key = ma.fields.Str(
        metadata={
            "doc": "Key under which the actual service config is registered in config"
        }
    )
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the service config class"},
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
        metadata={"doc": "Extra code to be put below the service config class"},
    )
    components = ma.fields.List(
        ma.fields.String(), metadata={"doc": "List of service components"}
    )
    generate_links = ma.fields.Bool(
        attribute="generate-links",
        data_key="generate-links",
        metadata={"doc": "Generate links section (default)"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class ServiceModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, AppModelComponent]

    class ModelSchema(ma.Schema):
        service = ma.fields.Nested(
            ServiceClassSchema, metadata={"doc": "Service settings"}
        )
        service_config = ma.fields.Nested(
            ServiceConfigClassSchema,
            attribute="service-config",
            data_key="service-config",
            metadata={"doc": "Service config settings"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        profile_module = context["profile_module"]
        module = datatype.definition["module"]["qualified"]
        module_base_upper = datatype.definition["module"]["base-upper"]
        record_prefix = datatype.definition["module"]["prefix"]
        flask_extension_name = datatype.definition["ext"]["alias"]

        service_package = f"{module}.services.{profile_module}"

        config = set_default(datatype, "service-config", {})

        config.setdefault("generate", True)
        config.setdefault(
            "config-key",
            f"{module_base_upper}_{context['profile_upper']}_SERVICE_CONFIG",
        )
        config_module = config.setdefault(
            "module",
            f"{service_package}.config",
        )
        config.setdefault(
            "class",
            f"{config_module}.{record_prefix}ServiceConfig",
        )
        config.setdefault("generate-links", True)
        config.setdefault("extra-code", "")
        config.setdefault("service-id", flask_extension_name)
        config.setdefault("base-classes", ["RecordServiceConfig"])
        config.setdefault("components", [])
        config.setdefault(
            "imports",
            [{"import": "invenio_records_resources.services.RecordServiceConfig"}],
        )
        convert_config_to_qualified_name(config)

        service = set_default(datatype, "service", {})

        service.setdefault("generate", True)
        service.setdefault(
            "config-key",
            f"{module_base_upper}_{context['profile_upper']}_SERVICE_CLASS",
        )
        service.setdefault("proxy", f"current_service")
        service_module = service.setdefault("module", f"{service_package}.service")
        service.setdefault("class", f"{service_module}.{record_prefix}Service")
        service.setdefault("extra-code", "")
        service.setdefault("base-classes", ["RecordService"])
        service.setdefault(
            "imports", [{"import": "invenio_records_resources.services.RecordService"}]
        )
        convert_config_to_qualified_name(service)