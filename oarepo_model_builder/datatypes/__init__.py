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


from .datatypes import DataType, datatypes, Import
from .primitive_types import (
    NumberDataType,  # noqa
    IntegerDataType,
    FloatDataType,
    DoubleDataType,
    BooleanDataType,
)

from .strings import (
    StringDataType,  # noqa
    FulltextDataType,
    KeywordDataType,
    FulltextKeywordDataType,
)

from .containers import (
    ObjectDataType,
    NestedDataType,
    FlattenDataType,
    ArrayDataType,
)

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
    ArrayDataType,
]
