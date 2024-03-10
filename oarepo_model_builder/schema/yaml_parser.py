
from ruamel.yaml import CommentedMap, CommentedSeq

from oarepo_model_builder.schema.value import SchemaValue


def convert_ruamel_to_schema_value(data, source, lc, parent):
    if isinstance(data, CommentedMap):
        sv = SchemaValue({}, data.lc.line, data.lc.col, source, parent)
        for k, v in data.items():
            sv.value[k] = convert_ruamel_to_schema_value(v, source, data.lc, sv)
        return sv
    if isinstance(data, CommentedSeq):
        sv = SchemaValue([], data.lc.line, data.lc.col, source, parent)
        for v in data:
            sv.value.append(convert_ruamel_to_schema_value(v, source, data.lc, sv))
        return sv
    return SchemaValue(data, lc.line, lc.col, source, parent)
