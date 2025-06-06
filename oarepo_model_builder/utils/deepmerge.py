import copy
from typing import Union


def remove_colon_prefix(data):

    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if ":" in k:
                k = k.split(":", 1)[1]
            new_data[k] = remove_colon_prefix(v)
        return new_data
    else:
        return data


def deepmerge(
    target,
    source,
    stack=None,
    listmerge: Union[str, callable] = "overwrite",
    dictmerge=None,
):
    if stack is None:
        stack = []

    if isinstance(target, dict):
        if source is not None:
            if not isinstance(source, dict):
                raise AttributeError(
                    f"Incompatible source and target on path {stack}: source {source}, target {target}"
                )
            if dictmerge:
                merged = dictmerge(target, source, stack)
            else:
                merged = None
            if merged is None:
                for k, v in list(source.items()):
                    _source = source
                    if ":" in k:
                        key = k
                        k = key.split(":")[1]
                        listmerge = key.split(":")[0]
                        _source[k] = _source.pop(key)

                    if k not in target:
                        target[k] = remove_colon_prefix(source[k])
                    else:
                        target[k] = deepmerge(
                            target[k],
                            _source[k],
                            stack + [k],
                            listmerge=listmerge,
                            dictmerge=dictmerge,
                        )
    elif isinstance(target, list):
        if source is not None:
            if isinstance(source, dict):
                raise AttributeError(
                    f"Incompatible source and target on path {stack}: source {source}, target {target}"
                )
            if not isinstance(source, list):
                return target
            if listmerge == "overwrite":
                for idx in range(min(len(source), len(target))):
                    target[idx] = deepmerge(
                        target[idx],
                        source[idx],
                        stack + [idx],
                        listmerge=listmerge,
                        dictmerge=dictmerge,
                    )
                for idx in range(len(target), len(source)):
                    target.append(source[idx])
            elif listmerge == "extend":
                target.extend(source)
            elif listmerge == "prepend":
                target = source + target
            elif listmerge == "keep":
                if len(source) > len(target):
                    target.extend(source[len(target) :])
            elif callable(listmerge):
                listmerge(target, source, stack)
            else:
                raise AttributeError(
                    'listmerge must be one of "overwrite", "extend" or "keep"'
                )
    elif target is None:
        return copy.deepcopy(source)
    return target
