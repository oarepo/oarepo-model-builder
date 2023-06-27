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
    proxy = ma.fields.Str(
        metadata={"doc": "name of the service proxy, will be put to _proxies_ package"}
    )
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
    skip = ma.fields.Boolean()


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
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    skip = ma.fields.Boolean()


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
        config.setdefault("extra-code", "")
        config.setdefault("service-id", datatype.definition["module"]["suffix-snake"])
        config.setdefault(
            "base-classes",
            ["PermissionsPresetsConfigMixin", "InvenioRecordServiceConfig"],
        )
        config.setdefault("components", [])
        config.setdefault(
            "imports",
            [
                {
                    "import": "invenio_records_resources.services.RecordServiceConfig",
                    "alias": "InvenioRecordServiceConfig",
                },
                {
                    "import": "oarepo_runtime.config.service.PermissionsPresetsConfigMixin"
                },
            ],
        )
        convert_config_to_qualified_name(config)

        service = set_default(datatype, "service", {})

        service.setdefault("generate", True)
        service.setdefault(
            "config-key",
            f"{module_base_upper}_{context['profile_upper']}_SERVICE_CLASS",
        )
        service.setdefault("proxy", "current_service")
        service_module = service.setdefault("module", f"{service_package}.service")
        service.setdefault("class", f"{service_module}.{record_prefix}Service")
        service.setdefault("extra-code", "")
        service.setdefault("base-classes", ["InvenioRecordService"])
        service.setdefault(
            "imports",
            [
                {
                    "import": "invenio_records_resources.services.RecordService",
                    "alias": "InvenioRecordService",
                }
            ],
        )
        convert_config_to_qualified_name(service)
