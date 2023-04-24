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


from .containers import (
    ArrayDataType,
    FlattenDataType,
    NestedDataType,
    ObjectDataType,
)  # noqa
from .model import ModelDataType  # noqa
from .datatypes import DataType, Import, datatypes, DataTypeComponent, Section  # noqa
from .dates import (
    DateDataType,
    DateTimeDataType,
    EDTFDataType,
    EDTFIntervalType,
    TimeDataType,
)  # noqa
from .primitive_types import NumberDataType  # noqa , just for export
from .primitive_types import (
    BooleanDataType,
    DoubleDataType,
    FloatDataType,
    IntegerDataType,
)
from .strings import StringDataType  # noqa , just for export
from .strings import (
    FulltextDataType,
    FulltextKeywordDataType,
    KeywordDataType,
    URLDataType,
)  # noqa

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
    URLDataType,
    ModelDataType,
]
