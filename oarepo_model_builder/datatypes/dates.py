from typing import List

from .datatypes import DataType, Import


class BaseDateDataType(DataType):
    marshmallow_field = "ma_fields.String"


class DateDataType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date"
    ui_marshmallow_field = "l10n.LocalizedDate"
    model_type = "date"
    default_facet_class = "DateFacet"
    default_facet_imports = [{"import": "oarepo_runtime.facets.date.DateFacet"}]

    def mapping(self, **extras):
        return super().mapping(format="strict_date", **extras)

    def json_schema(self, **extras):
        return super().json_schema(format="date", **extras)

    def marshmallow_validators(self) -> List[str]:
        return super().marshmallow_validators() + [
            "validate_date('%Y-%m-%d')",
        ]

    def imports(self, *extra) -> List[Import]:
        return super().imports(
            Import(import_path="oarepo_runtime.validation.validate_date", alias=None),
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
        )


class TimeDataType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date"
    model_type = "time"
    ui_marshmallow_field = "l10n.LocalizedTime"
    default_facet_class = "TimeFacet"
    default_facet_imports = [{"import": "oarepo_runtime.facets.date.TimeFacet"}]

    def mapping(self, **extras):
        return super().mapping(format="strict_time||strict_time_no_millis")

    def json_schema(self, **extras):
        return super().json_schema(format="time", **extras)

    def marshmallow_validators(self) -> List[str]:
        return super().marshmallow_validators() + [
            "validate_date('%H:%M:%S')",
        ]

    def imports(self, *extra) -> List[Import]:
        return super().imports(
            Import(import_path="oarepo_runtime.validation.validate_date", alias=None),
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
        )


class DateTimeDataType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date"
    marshmallow_field = "ma_fields.String"
    model_type = "datetime"
    ui_marshmallow_field = "l10n.LocalizedDateTime"
    default_facet_class = "DateTimeFacet"
    default_facet_imports = [{"import": "oarepo_runtime.facets.date.DateTimeFacet"}]

    def mapping(self, **extras):
        return super().mapping(format="strict_date_time||strict_date_time_no_millis")

    def json_schema(self, **extras):
        return super().json_schema(format="date-time", **extras)

    def marshmallow_validators(self) -> List[str]:
        return super().marshmallow_validators() + [
            "validate_datetime",
        ]

    def imports(self, *extra) -> List[Import]:
        return super().imports(
            Import(
                import_path="oarepo_runtime.validation.validate_datetime", alias=None
            ),
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
        )


class EDTFDataType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date"
    model_type = "edtf"
    marshmallow_field = "TrimmedString"
    ui_marshmallow_field = "l10n.LocalizedEDTF"
    default_facet_class = "EDTFFacet"
    default_facet_imports = [{"import": "oarepo_runtime.facets.date.EDTFFacet"}]

    def mapping(self, **extras):
        return super().mapping(
            format="strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy"
        )

    def marshmallow_validators(self):
        return super().marshmallow_validators() + [
            "CachedMultilayerEDTFValidator(types=(EDTFDate,))"
        ]

    def imports(self, *_extra) -> List[Import]:
        return super().imports(
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
            Import(import_path="edtf.Date", alias="EDTFDate"),
            Import(
                import_path="oarepo_runtime.validation.CachedMultilayerEDTFValidator",
                alias=None,
            ),
            Import(import_path="marshmallow_utils.fields.trimmed.TrimmedString", alias=None)
        )


class EDTFIntervalType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date_range"
    model_type = "edtf-interval"
    ui_marshmallow_field = "l10n.LocalizedEDTFInterval"
    marshmallow_field = "TrimmedString"
    default_facet_class = "EDTFIntervalFacet"
    default_facet_imports = [{"import": "oarepo_runtime.facets.date.EDTFIntervalFacet"}]

    def mapping(self, **extras):
        return super().mapping(
            format="strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy"
        )

    def marshmallow_validators(self):
        return super().marshmallow_validators() + [
            "CachedMultilayerEDTFValidator(types=(EDTFInterval,))"
        ]

    def imports(self, *extra):
        return super().imports(
            Import(import_path="edtf.Interval", alias="EDTFInterval"),
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
            Import(
                import_path="oarepo_runtime.validation.CachedMultilayerEDTFValidator",
                alias=None,
            ),
            Import(import_path="marshmallow_utils.fields.trimmed.TrimmedString", alias=None),
            *extra,
        )
