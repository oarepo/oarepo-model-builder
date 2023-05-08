from typing import Iterable, List


def dict_get(data, path: Iterable[str]):
    for p in path:
        if not data:
            data = {}
        data = data.get(p)
    return data


def dict_setdefault(data, path: List[str], default=None):
    for p in path[:-1]:
        r = data.get(p)
        if not data:
            data.setdefault(p, {})
        data = r
    if path[-1] not in data:
        data[path[-1]] = default
    return data[path[-1]]
