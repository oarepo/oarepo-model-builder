from .datatypes import DataType


class BaseDateDataType(DataType):
    marshmallow = {"field-class": "ma.fields.String"}

    facets = {
        "facet-class": "DateTimeFacet",
        "imports": [{"import": "oarepo_runtime.facets.date.DateTimeFacet"}],
    }


class DateDataType(BaseDateDataType):
    model_type = "date"
    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedDate",
            "imports": [
                {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}  # NOSONAR
            ],
        }
    }
    marshmallow = {
        "field-class": "ma.fields.String",
        "validators": ["validate_date('%Y-%m-%d')"],
        "imports": [{"import": "oarepo_runtime.validation.validate_date"}],
    }
    mapping = {"type": "date", "format": "basic_date||strict_date"}
    json_schema = {"type": "string", "format": "date"}


class TimeDataType(BaseDateDataType):
    model_type = "time"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedTime",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "ma.fields.String",
        "validators": ["validate_date('%H:%M:%S')"],
        "imports": [{"import": "oarepo_runtime.validation.validate_date"}],
    }
    mapping = {
        "type": "date",
        "format": "strict_time||strict_time_no_millis||basic_time||basic_time_no_millis",
    }
    json_schema = {"type": "string", "format": "time"}


class DateTimeDataType(BaseDateDataType):
    model_type = "datetime"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedDateTime",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "ma.fields.String",
        "validators": ["validate_datetime"],
        "imports": [{"import": "oarepo_runtime.validation.validate_datetime"}],
    }
    mapping = {
        "type": "date",
        "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
    }
    json_schema = {"type": "string", "format": "date-time"}


class EDTFDataType(BaseDateDataType):
    model_type = "edtf"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedEDTF",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "TrimmedString",
        "validators": ["CachedMultilayerEDTFValidator(types=(EDTFDate,))"],
        "imports": [
            {"import": "oarepo_runtime.validation.CachedMultilayerEDTFValidator"},
            {"import": "edtf.Date", "alias": "EDTFDate"},
            {"import": "marshmallow_utils.fields.TrimmedString"},
        ],
    }
    mapping = {
        "type": "date",
        "format": "strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy",
    }
    json_schema = {"type": "string", "format": "date-time"}


class EDTFIntervalType(BaseDateDataType):
    model_type = "edtf-interval"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedEDTFInterval",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "TrimmedString",
        "validators": ["CachedMultilayerEDTFValidator(types=(EDTFInterval,))"],
        "imports": [
            {"import": "oarepo_runtime.validation.CachedMultilayerEDTFValidator"},
            {"import": "edtf.Interval", "alias": "EDTFInterval"},
            {"import": "marshmallow_utils.fields.TrimmedString"},
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
