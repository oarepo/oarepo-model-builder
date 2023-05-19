import json


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


def array_contains_value(arr, value):
    if isinstance(value, (int, float, bool, str)):
        return value in arr
    pv = json.dumps(value, sort_keys=True)
    for vv in arr:
        vv = json.dumps(vv, sort_keys=True)
        if vv == pv:
            return True
    return False


def deep_equals(value, value2):
    if isinstance(value, (int, float, bool, str)):
        return value == value2
    return json.dumps(value, sort_keys=True) == json.dumps(value2, sort_keys=True)


def append_array(datatype, *attrs):
    arr = set_default(datatype, *attrs[:-1], [])
    value = attrs[-1]
    if callable(value):
        value = value(datatype.definition)
    if not array_contains_value(arr, value):
        arr.append(value)


def prepend_array(datatype, *attrs):
    arr = set_default(datatype, *attrs[:-1], [])
    value = attrs[-1]
    if callable(value):
        value = value(datatype.definition)
    if not array_contains_value(arr, value):
        arr.insert(0, value)


def place_after(datatype, *attrs):
    value = attrs[-1]
    placeholder = attrs[-2]
    arr = set_default(datatype, *attrs[:-2], [])
    if callable(value):
        value = value(datatype.definition)
    if callable(placeholder):
        placeholder = placeholder(datatype.definition)
    if not array_contains_value(arr, value):
        for idx, elem in enumerate(arr):
            if deep_equals(placeholder, elem):
                arr.insert(idx + 1, value)
                break
