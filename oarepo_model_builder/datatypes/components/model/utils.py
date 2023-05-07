def set_default(datatype, *attrs):
    keys = attrs[:-1]
    value = attrs[-1]
    d = datatype.definition
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
            d = d[k]
    if keys[-1] not in d:
        if callable(value):
            value = value(datatype.definition)
        d[keys[-1]] = value
        return value
    return d[keys[-1]]


def append_array(datatype, *attrs):
    arr = set_default(datatype, *attrs[:-1], [])
    value = attrs[-1]
    if callable(value):
        value = value(datatype.definition)
    if value not in arr:
        arr.append(value)


def prepend_array(datatype, *attrs):
    arr = set_default(datatype, *attrs[:-1], [])
    value = attrs[-1]
    if callable(value):
        value = value(datatype.definition)
    if value not in arr:
        arr.insert(0, value)
