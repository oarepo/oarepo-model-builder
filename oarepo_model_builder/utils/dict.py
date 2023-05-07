from typing import Iterable


def dict_get(data, path: Iterable[str]):
    for p in path:
        if not data:
            data = {}
        data = data.get(p)
    return data
