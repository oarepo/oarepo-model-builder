from .datatypes import DataType


class BaseDateDataType(DataType):
    marshmallow = {"field-class": "ma_fields.String"}


class DateDataType(BaseDateDataType):
    model_type = "date"
    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedDate",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "ma_fields.String",
        "validators": ["validate_date('%Y-%m-%d')"],
        "imports": [{"import": "oarepo_runtime.validation.validate_date"}],
    }
    mapping = {"type": "date", "format": "strict_date"}
    json_schema = {"type": "string", "format": "date"}

    # default_facet_class = "DateFacet"
    # default_facet_imports = [{"import": "oarepo_runtime.facets.date.DateFacet"}]


class TimeDataType(BaseDateDataType):
    model_type = "time"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedTime",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "ma_fields.String",
        "validators": ["validate_date('%H:%M:%S')"],
        "imports": [{"import": "oarepo_runtime.validation.validate_date"}],
    }
    mapping = {"type": "date", "format": "strict_time||strict_time_no_millis"}
    json_schema = {"type": "string", "format": "time"}

    # default_facet_class = "TimeFacet"
    # default_facet_imports = [{"import": "oarepo_runtime.facets.date.TimeFacet"}]


class DateTimeDataType(BaseDateDataType):
    # marshmallow_field = "ma_fields.String"
    model_type = "datetime"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedDateTime",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "ma_fields.String",
        "validators": ["validate_datetime"],
        "imports": [{"import": "oarepo_runtime.validation.validate_datetime"}],
    }
    mapping = {"type": "date", "format": "strict_date_time||strict_date_time_no_millis"}
    json_schema = {"type": "string", "format": "date-time"}

    # default_facet_class = "DateTimeFacet"
    # default_facet_imports = [{"import": "oarepo_runtime.facets.date.DateTimeFacet"}]


class EDTFDataType(BaseDateDataType):
    model_type = "edtf"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedEDTF",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "ma_fields.String",
        "validators": ["CachedMultilayerEDTFValidator(types=(EDTFDate,))"],
        "imports": [
            {"import": "oarepo_runtime.validation.CachedMultilayerEDTFValidator"},
            {"import": "edtf.Date", "alias": "EDTFDate"},
        ],
    }
    mapping = {
        "type": "date",
        "format": "strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy",
    }
    json_schema = {"type": "string", "format": "date-time"}

    # default_facet_class = "EDTFFacet"
    # default_facet_imports = [{"import": "oarepo_runtime.facets.date.EDTFFacet"}]


class EDTFIntervalType(BaseDateDataType):
    model_type = "edtf-interval"

    ui = {
        "marshmallow": {
            "field-class": "l10n.LocalizedEDTFInterval",
            "imports": [{"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"}],
        }
    }
    marshmallow = {
        "field-class": "ma_fields.String",
        "validators": ["CachedMultilayerEDTFValidator(types=(EDTFInterval,))"],
        "imports": [
            {"import": "oarepo_runtime.validation.CachedMultilayerEDTFValidator"},
            {"import": "edtf.Interval", "alias": "EDTFInterval"},
        ],
    }
    mapping = {
        "type": "date_range",
        "format": "strict_date_time||strict_date_time_no_millis||strict_date||yyyy-MM||yyyy",
    }
    json_schema = {"type": "string", "format": "date-time"}

    # default_facet_class = "EDTFIntervalFacet"
    # default_facet_imports = [{"import": "oarepo_runtime.facets.date.EDTFIntervalFacet"}]
