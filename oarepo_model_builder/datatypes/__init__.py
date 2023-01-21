"""
Datatypes supported out of the box:

integer, float, double:
  constraints: minimumExclusive, maximumExclusive, minimum, maximum

boolean:
  no constraints supported

date, time, datetime
  no constraints supported

edtf, edtf-interval
  no constraints supported

fulltext, keyword, fulltext+keyword:
  minLength, maxLength, pattern

flatten:
  object represented as flatten type in elasticsearch
"""


from .datatypes import DataType, datatypes
from .primitive_types import (
    NumberDataType,
    IntegerDataType,
    FloatDataType,
    DoubleDataType,
    BooleanDataType,
)

from .strings import (
    StringDataType,
    FulltextDataType,
    KeywordDataType,
    FulltextKeywordDataType,
)

from .containers import ObjectDataType, NestedDataType, FlattenDataType

from .dates import (
    DateDataType,
    TimeDataType,
    DateTimeDataType,
    EDTFDataType,
    EDTFIntervalType,
)

DEFAULT_DATATYPES = [
    IntegerDataType,
    FloatDataType,
    DoubleDataType,
    BooleanDataType,
    DateDataType,
    TimeDataType,
    DateTimeDataType,
    EDTFDataType,
    EDTFIntervalType,
    FulltextDataType,
    KeywordDataType,
    FulltextKeywordDataType,
    ObjectDataType,
    NestedDataType,
    FlattenDataType,
]

__all__ = [
    "DataType",
    "datatypes",
    "DEFAULT_DATATYPES",
    "NumberDataType",
    "IntegerDataType",
    "FloatDataType",
    "DoubleDataType",
    "BooleanDataType",
    "DateDataType",
    "TimeDataType",
    "DateTimeDataType",
    "EDTFDataType",
    "EDTFIntervalType",
    "StringDataType",
    "FulltextDataType",
    "KeywordDataType",
    "FulltextKeywordDataType",
    "ObjectDataType",
    "NestedDataType",
    "FlattenDataType",
]
