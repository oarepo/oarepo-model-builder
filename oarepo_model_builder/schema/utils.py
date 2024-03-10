def resolve_id(json, element_id):
    if isinstance(json, dict):
        if "$id" in json and json["$id"] == element_id:
            return json
        continue_with = json.values()
    elif isinstance(json, (tuple, list)):
        continue_with = json
    else:
        return None
    for k in continue_with:
        ret = resolve_id(k, element_id)
        if ret is not None:
            return ret


def remove_star_keys(schema):
    if isinstance(schema, dict):
        for k, v in list(schema.items()):
            if k.startswith("*"):
                del schema[k]
            else:
                remove_star_keys(v)
    elif isinstance(schema, (list, tuple)):
        for k in schema:
            remove_star_keys(k)


def use_star_keys(schema):
    if isinstance(schema, dict):
        for k, v in list(schema.items()):
            if k.startswith("*"):
                del schema[k]
                schema[k[1:]] = v
        for v in schema.values():
            use_star_keys(v)
    elif isinstance(schema, (list, tuple)):
        for k in schema:
            use_star_keys(k)
