from .datatypes import DataType


class StringDataType(DataType):
    @property
    def marshmallow_validators(self):
        validators = []
        ranges = {}
        for param, schema in (
            ("min", "minLength"),
            ("max", "maxLength"),
        ):
            if schema in self.definition:
                ranges[param] = self.definition[schema]

        if ranges:
            params = ", ".join(f"{k}={v}" for k, v in ranges.items())
            validators.append(f"ma_validate.Length({params})")

        if "pattern" in self.definition:
            pattern = self.definition["pattern"]
            pattern = pattern.replace("\\", "\\\\")
            pattern = pattern.replace('"', '\\"')
            validators.append(f'ma_validate.Regexp("{pattern}")')

        return validators


class FulltextDataType(StringDataType):
    schema_type = "string"
    mapping_type = "text"
    marshmallow_field = "ma_fields.Str"
    model_type = "fulltext"


class KeywordDataType(StringDataType):
    schema_type = "string"
    mapping_type = "keyword"
    marshmallow_field = "ma_fields.Str"
    model_type = "keyword"


class FulltextKeywordDataType(StringDataType):
    schema_type = "string"
    mapping_type = "text"
    marshmallow_field = "ma_fields.Str"
    model_type = "fulltext+keyword"

    def mapping(self):
        ret = super().mapping()
        ret.setdefault("fields", {}).setdefault("keyword", {"type": "keyword"})
