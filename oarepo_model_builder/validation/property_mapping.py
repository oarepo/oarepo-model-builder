import marshmallow as ma

from .utils import ExtendablePartSchema


class PropertyMapping(ExtendablePartSchema):
    class Meta:
        unknown = ma.INCLUDE
