def deepmerge(target, source, stack=None, listmerge="overwrite"):
    if stack is None:
        stack = []

    if isinstance(target, dict):
        if source is not None:
            if not isinstance(source, dict):
                raise AttributeError(
                    f"Incompatible source and target on path {stack}: source {source}, target {target}"
                )
            for k, v in source.items():
                if k not in target:
                    target[k] = source[k]
                else:
                    target[k] = deepmerge(
                        target[k], source[k], stack + [k], listmerge=listmerge
                    )
    elif isinstance(target, list):
        if source is not None:
            if not isinstance(source, list):
                raise AttributeError(
                    f"Incompatible source and target on path {stack}: source {source}, target {target}"
                )
            if listmerge == "overwrite":
                for idx in range(min(len(source), len(target))):
                    target[idx] = deepmerge(
                        target[idx], source[idx], stack + [idx], listmerge=listmerge
                    )
                for idx in range(len(target), len(source)):
                    target.append(source[idx])
            elif listmerge == "extend":
                target.extend(source)
            elif listmerge == "keep":
                if len(source) > len(target):
                    target.extend(source[len(target) :])
            else:
                raise AttributeError(
                    'listmerge must be one of "overwrite", "extend" or "keep"'
                )
    return target
