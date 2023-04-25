import re

from marshmallow import fields
from marshmallow.exceptions import ValidationError

from .datatypes import DataType


def validate_regex(value):
    if not value:
        return
    try:
        re.compile(value)
    except Exception as e:
        raise ValidationError(
            f"Regex '{value}' is not valid. Reported error: '{str(e)}'"
        )


class StringDataType(DataType):
    ui = {
        "marshmallow": {
            "field-class": "ma_fields.String",
        }
    }
    marshmallow = {
        "field-class": "ma_fields.String",
    }
    json_schema = {"type": "string"}

    class ModelSchema(DataType.ModelSchema):
        minLength = fields.Integer(required=False)
        maxLength = fields.Integer(required=False)
        regex = fields.String(required=False, validate=validate_regex)
        # enum = fields.List(fields.String(), required=False)

    # def marshmallow_validators(self):
    #     validators = []
    #     ranges = {}
    #     for param, schema in (
    #         ("min", "minLength"),
    #         ("max", "maxLength"),
    #     ):
    #         if schema in self.definition:
    #             ranges[param] = self.definition[schema]

    #     if ranges:
    #         params = ", ".join(f"{k}={v}" for k, v in ranges.items())
    #         validators.append(f"ma_validate.Length({params})")

    #     if "pattern" in self.definition:
    #         pattern = self.definition["pattern"]
    #         pattern = pattern.replace("\\", "\\\\")
    #         pattern = pattern.replace('"', '\\"')
    #         validators.append(f'ma_validate.Regexp("{pattern}")')

    #     return validators

    # @property
    # def ui_marshmallow_field(self):
    #     if "enum" in self.definition:
    #         return "l10n.LocalizedEnum"
    #     return self.marshmallow_field

    # def ui_marshmallow(self, **extras):
    #     ret = super().ui_marshmallow(**extras)
    #     if "enum" in self.definition:
    #         # TODO: allow for custom prefix
    #         gettext_prefix = self.model.get("package")
    #         ret.setdefault("arguments", []).extend(
    #             [
    #                 f'value_prefix="{gettext_prefix}"',
    #             ]
    #         )
    #     return ret

    # def imports(self, *extra) -> List[Import]:
    #     if "enum" in self.definition:
    #         return super().imports(
    #             *extra,
    #             Import(
    #                 import_path="oarepo_runtime.ui.marshmallow",
    #                 alias="l10n",
    #             ),
    #         )
    #     else:
    #         return super().imports(*extra)


class FulltextDataType(StringDataType):
    model_type = "fulltext"
    mapping = {"type": "text"}

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     "fulltext can not have facet"
    #     return []


class KeywordDataType(StringDataType):
    model_type = "keyword"
    mapping = {"type": "keyword"}

    # @property
    # def facet_class(self):
    #     if self.definition.get("enum"):
    #         return "EnumTermsFacet"
    #     return super().facet_class

    # @property
    # def facet_imports(self):
    #     if self.definition.get("enum"):
    #         return [{"import": "oarepo_runtime.facets.enum.EnumTermsFacet"}]
    #     return super().facet_imports


class FulltextKeywordDataType(StringDataType):
    model_type = "fulltext+keyword"
    mapping = {"type": "text", "fields": {"keyword": {"type": "keyword"}}}

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     return super().get_facet(stack, parent_path, (path_suffix or "") + ".keyword")


class URLDataType(StringDataType):
    model_type = "url"
    mapping = {"type": "keyword"}
