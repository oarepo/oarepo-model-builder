from .datatypes import DataType


class BaseDateDataType(DataType):
    marshmallow = {"field-class": "marshmallow.fields{ma_fields.String}"}

    facets = {
        "facet-class": "oarepo_runtime.services.facets.date.DateTimeFacet",
    }


class DateDataType(BaseDateDataType):
    model_type = "date"
    ui = {
        "marshmallow": {
            "field-class": "oarepo_runtime.services.schema.ui.LocalizedDate",
        }
    }
    marshmallow = {
        "field-class": "marshmallow.fields{ma_fields.String}",
        "validators": [
            "{{oarepo_runtime.services.schema.validation.validate_date}}('%Y-%m-%d')"
        ],
    }
    mapping = {"type": "date", "format": "basic_date||strict_date"}
    json_schema = {"type": "string", "format": "date"}


class TimeDataType(BaseDateDataType):
    model_type = "time"

    ui = {
        "marshmallow": {
            "field-class": "oarepo_runtime.services.schema.ui.LocalizedTime",
        }
    }
    marshmallow = {
        "field-class": "marshmallow.fields{ma_fields.String}",
        "validators": [
            "{{oarepo_runtime.services.schema.validation.validate_date}}('%H:%M:%S')"
        ],
    }
    mapping = {
        "type": "date",
        "format": "strict_time||strict_time_no_millis||basic_time||basic_time_no_millis||hour_minute_second||hour||hour_minute",
    }
    json_schema = {"type": "string", "format": "time"}


class DateTimeDataType(BaseDateDataType):
    model_type = "datetime"

    ui = {
        "marshmallow": {
            "field-class": "oarepo_runtime.services.schema.ui.LocalizedDateTime",
        }
    }
    marshmallow = {
        "field-class": "marshmallow.fields{ma_fields.String}",
        "validators": [
            "{{oarepo_runtime.services.schema.validation.validate_datetime}}"
        ],
    }
    mapping = {
        "type": "date",
        "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
    }
    json_schema = {"type": "string", "format": "date-time"}


class EDTFTimeDataType(BaseDateDataType):
    model_type = "edtf-time"

    ui = {
        "marshmallow": {
            "field-class": "oarepo_runtime.services.schema.ui.LocalizedEDTFTime",
        }
    }
    marshmallow = {
        "field-class": "marshmallow_utils.fields.TrimmedString",
        "validators": [
            "{{oarepo_runtime.services.schema.validation.CachedMultilayerEDTFValidator}}(types=({{edtf.DateAndTime{EDTFDateAndTime} }}, {{edtf.Date{EDTFDate} }},))"
        ],
    }
    mapping = {
        "type": "date",
        "format": "strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy",
    }
    json_schema = {"type": "string", "format": "date-time"}


class EDTFTimeIntervalType(BaseDateDataType):
    model_type = "edtf-time-interval"

    ui = {
        "marshmallow": {
            "field-class": "oarepo_runtime.services.schema.ui.LocalizedEDTFTimeInterval",
        }
    }
    marshmallow = {
        "field-class": "marshmallow_utils.fields.TrimmedString",
        "validators": [
            "{{oarepo_runtime.services.schema.validation.CachedMultilayerEDTFValidator}}(types=({{edtf.EDTFObject{EDTFDateAndTime} }}, {{edtf.Date{EDTFDate} }}, {{edtf.Interval{EDTFInterval} }},))"
        ],
    }
    mapping = {
        "type": "date_range",
        "format": "strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy",
    }
    facets = {
        "searchable": False,  # it seems that facet on edtf is not supported in opensearch
    }
    json_schema = {"type": "string", "format": "date-time"}


class EDTFDataType(BaseDateDataType):
    model_type = "edtf"

    ui = {
        "marshmallow": {
            "field-class": "oarepo_runtime.services.schema.ui.LocalizedEDTF",
        }
    }
    marshmallow = {
        "field-class": "marshmallow_utils.fields.TrimmedString",
        "validators": [
            "{{oarepo_runtime.services.schema.validation.CachedMultilayerEDTFValidator}}(types=({{edtf.Date{EDTFDate} }},))"
        ],
    }
    mapping = {
        "type": "date",
        "format": "strict_date||yyyy-MM||yyyy",
    }
    json_schema = {"type": "string", "format": "date"}


class EDTFIntervalType(BaseDateDataType):
    model_type = "edtf-interval"

    ui = {
        "marshmallow": {
            "field-class": "oarepo_runtime.services.schema.ui.LocalizedEDTFInterval",
        }
    }
    marshmallow = {
        "field-class": "marshmallow_utils.fields.TrimmedString",
        "validators": [
            "{{oarepo_runtime.services.schema.validation.CachedMultilayerEDTFValidator}}(types=({{edtf.Interval{EDTFInterval} }},))"
        ],
    }
    mapping = {
        "type": "date_range",
        "format": "strict_date||yyyy-MM||yyyy",
    }
    facets = {
        "searchable": False,  # it seems that facet on edtf is not supported in opensearch
    }
    json_schema = {"type": "string", "format": "date"}
