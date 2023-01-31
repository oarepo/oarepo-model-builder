from marshmallow import fields

from .utils import ExtendablePartSchema
import enum


class OrderEnum(enum.Enum):
    asc = "asc"
    desc = "desc"


class PropertySortable(ExtendablePartSchema):
    key = fields.String(required=False)
    order = fields.Enum(
        OrderEnum,
        dump_default=OrderEnum.asc,
    )
