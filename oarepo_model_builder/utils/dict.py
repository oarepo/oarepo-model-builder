from typing import List


def dict_get(data, path: List[str], default=None):
    for p in path[:-1]:
        if not data:
            data = {}
        data = data.get(p)
    return (data or {}).get(path[-1], default)


def dict_setdefault(data, path: List[str], default=None):
    for p in path[:-1]:
        r = data.get(p)
        if not data:
            data.setdefault(p, {})
        data = r
    if path[-1] not in data:
        data[path[-1]] = default
    return data[path[-1]]
