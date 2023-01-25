from typing import List

from .datatypes import DataType, Import


class DateDataType(DataType):
    schema_type = "string"
    mapping_type = "date"
    marshmallow_field = "ma_fields.String"
    model_type = "date"

    def mapping(self, **extras):
        return super().mapping(format="strict_date", **extras)

    def json_schema(self, **extras):
        return super().json_schema(format="date", **extras)

    def marshmallow_validators(self) -> List[str]:
        return super().marshmallow_validators() + [
            # TODO: raise correct exception here
            "validate_date('%Y:%m:%d')",
        ]

    def imports(self, *extra) -> List[Import]:
        return super().imports(
            Import(import_path="oarepo_runtime.validation.validate_date", alias=None)
        )


class TimeDataType(DataType):
    schema_type = "string"
    mapping_type = "date"
    marshmallow_field = "ma_fields.Str"
    model_type = "time"

    def mapping(self, **extras):
        return super().mapping(format="strict_time||strict_time_no_millis")

    def json_schema(self, **extras):
        return super().json_schema(format="time", **extras)

    def marshmallow_validators(self) -> List[str]:
        return super().marshmallow_validators() + [
            # TODO: raise correct exception here
            "validate_date('%H:%M:%S')",
        ]

    def imports(self, *extra) -> List[Import]:
        return super().imports(
            Import(import_path="oarepo_runtime.validation.validate_date", alias=None)
        )


class DateTimeDataType(DataType):
    schema_type = "string"
    mapping_type = "date"
    marshmallow_field = "mu_fields.ISODateString"
    model_type = "datetime"

    def mapping(self, **extras):
        return super().mapping(format="strict_date_time||strict_date_time_no_millis")

    def json_schema(self, **extras):
        return super().json_schema(format="date-time", **extras)


class EDTFDataType(DataType):
    schema_type = "string"
    mapping_type = "date"
    marshmallow_field = "ma_fields.Str"
    model_type = "edtf"

    def mapping(self, **extras):
        return super().mapping(
            format="strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy"
        )

    def marshmallow_validators(self):
        return super().marshmallow_validators() + [
            "mu_fields.EDTFValidator(types=EDTFDate)"
        ]

    def imports(self, *args):
        return super().imports(Import(name="edtf.Date", alias="EDTFDate"))


class EDTFIntervalType(DataType):
    schema_type = "string"
    mapping_type = "date_range"
    marshmallow_field = "ma_fields.Str"
    model_type = "edtf-interval"

    def mapping(self, **extras):
        return super().mapping(
            format="strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy"
        )

    def marshmallow_validators(self):
        return super().marshmallow_validators() + [
            "mu_fields.EDTFValidator(types=EDTFInterval)"
        ]

    def imports(self, *args):
        return super().imports(Import(name="edtf.Interval", alias="EDTFInterval"))
