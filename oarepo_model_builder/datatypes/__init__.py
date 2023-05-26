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


from .containers import (  # noqa
    ArrayDataType,
    FlattenDataType,
    NestedDataType,
    ObjectDataType,
)
from .datatypes import DataType, DataTypeComponent, Import, Section, datatypes  # noqa
from .dates import (  # noqa
    DateDataType,
    DateTimeDataType,
    EDTFDataType,
    EDTFIntervalType,
    TimeDataType,
)
from .model import ModelDataType  # noqa
from .primitive_types import NumberDataType  # noqa , just for export
from .primitive_types import (
    BooleanDataType,
    DoubleDataType,
    FloatDataType,
    IntegerDataType,
)
from .strings import StringDataType  # noqa , just for export
from .strings import (  # noqa
    FulltextDataType,
    FulltextKeywordDataType,
    KeywordDataType,
    URLDataType,
    UUIDDataType,
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
    UUIDDataType,
    ObjectDataType,
    NestedDataType,
    FlattenDataType,
    ArrayDataType,
    URLDataType,
    ModelDataType,
]
