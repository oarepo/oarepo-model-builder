from typing import List

from ..utils.facet_helpers import facet_definiton, facet_name
from .datatypes import DataType, Import


class BaseDateDataType(DataType):
    marshmallow_field = "ma_fields.String"

    def get_facet(self, stack, parent_path):
        key, field = facet_definiton(self)
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + "." + self.key
        elif self.key:
            path = self.key
        if field:
            return field, facet_name(path)
        else:
            return f'TermsFacet(field="{path}")', facet_name(path)


class DateDataType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date"
    ui_marshmallow_field = "l10n.LocalizedDate"
    model_type = "date"

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
    marshmallow_field = "mu_fields.ISODateString"
    model_type = "datetime"
    ui_marshmallow_field = "l10n.LocalizedDateTime"

    def mapping(self, **extras):
        return super().mapping(format="strict_date_time||strict_date_time_no_millis")

    def json_schema(self, **extras):
        return super().json_schema(format="date-time", **extras)

    def imports(self, *extra) -> List[Import]:
        return super().imports(
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
        )


class EDTFDataType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date"
    model_type = "edtf"
    ui_marshmallow_field = "l10n.LocalizedEDTF"

    def mapping(self, **extras):
        return super().mapping(
            format="strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy"
        )

    def marshmallow_validators(self):
        return super().marshmallow_validators() + [
            "mu_fields.EDTFValidator(types=EDTFDate)"
        ]

    def imports(self, *_extra) -> List[Import]:
        return super().imports(
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
            Import(import_path="edtf.Date", alias="EDTFDate"),
        )


class EDTFIntervalType(BaseDateDataType):
    schema_type = "string"
    mapping_type = "date_range"
    model_type = "edtf-interval"
    ui_marshmallow_field = "l10n.LocalizedEDTFInterval"

    def mapping(self, **extras):
        return super().mapping(
            format="strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy"
        )

    def marshmallow_validators(self):
        return super().marshmallow_validators() + [
            "mu_fields.EDTFValidator(types=EDTFInterval)"
        ]

    def imports(self, *extra):
        return super().imports(
            Import(import_path="edtf.Interval", alias="EDTFInterval"),
            Import(import_path="oarepo_runtime.ui.marshmallow", alias="l10n"),
            *extra,
        )
