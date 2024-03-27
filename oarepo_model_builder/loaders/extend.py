from oarepo_model_builder.schema.value import SchemaValue


def extend_modify_marshmallow(data: SchemaValue, **kwargs):
    roots = find_extend_roots(data)
    if not roots:
        return
    cache = {}
    for root in roots:
        # only object can be extended, so root has to point to object
        if "properties" not in root.value:
            raise ValueError(
                "Root of the merged schema with extended schema has to be "
                f"an object containing 'properties', but it is {root.value}"
            )
        modify_object_marshmallow(root, cache)


def modify_object_marshmallow(data: SchemaValue, cache):
    # if data contains only inherited properties, just mark the class as not-generated
    # and return
    modify_object_properties_marshmallow(data, cache)

    if contains_only_inherited_properties(data, cache):
        data.setdefault("marshmallow", {})["generate"] = False
        data.setdefault("ui", {}).setdefault("marshmallow", {})["generate"] = False
        return

    if contains_only_non_inherited_properties(data, cache):
        return

    # if the element is a mixture of inherited and new properties, we need to
    # convert it to a base class
    convert_to_base_class(data.setdefault("marshmallow", {}))
    convert_to_base_class(data.setdefault("ui", {}).setdefault("marshmallow", {}))

    # and set generate to True
    data["marshmallow"]["generate"] = True
    data["ui"]["marshmallow"]["generate"] = True


def convert_to_base_class(marshmallow):
    if "class" in marshmallow:
        if not marshmallow["class"].source.is_extended:
            # the class has been overwritten by a local one,
            # we want to add the previous class as a base class
            if (
                marshmallow["class"].previous
                and marshmallow["class"].previous.source.is_extended
            ):
                new_base_class = marshmallow["class"].previous
            else:
                raise NotImplementedError(
                    "The class has been overwritten by a local class, "
                    "but the previous class is not present or is not extended:\n{marshmallow}"
                )
        else:
            # the class comes from the extension, so pop it out
            # and use it inside base classes
            new_base_class = marshmallow.pop("class", None)
        marshmallow.setdefault("base-classes", []).append(new_base_class)
    else:
        raise ValueError(
            "You need to set a class name of the extended class to convert it to a base class."
            f"Currently there is: {marshmallow}"
        )


def modify_object_properties_marshmallow(data: SchemaValue, cache):
    # and go deeper to the properties
    for prop in data["properties"].values():
        modify_property_marshmallow(prop, cache)


def modify_property_marshmallow(data, cache):
    if not data.is_dict:
        return
    if "properties" in data:
        modify_object_marshmallow(data, cache)
    elif "items" in data:
        modify_list_marshmallow(data, cache)
    else:
        modify_primitive_marshmallow(data, cache)


def modify_list_marshmallow(data: SchemaValue, cache):
    if "items" in data:
        modify_property_marshmallow(data["items"], cache)


def modify_primitive_marshmallow(prop, cache):
    # if it is only inherited, do not generate
    if contains_only_inherited_properties(prop, cache):
        prop.setdefault("marshmallow", {})["read"] = False
        prop.setdefault("marshmallow", {})["write"] = False
        prop.setdefault("ui", {}).setdefault("marshmallow", {})["read"] = False
        prop.setdefault("ui", {}).setdefault("marshmallow", {})["write"] = False
    # otherwise do not modify


def contains_only_inherited_properties(data: SchemaValue, cache):
    if id(data) not in cache:
        fill_cache(data, cache)
    rec = cache[id(data)]
    return rec["not_inherited"] == 0


def contains_only_non_inherited_properties(data: SchemaValue, cache):
    if id(data) not in cache:
        fill_cache(data, cache)
    rec = cache[id(data)]
    return rec["inherited"] == 0


def fill_cache(data, cache):
    if data.is_dict:
        ret = fill_cache_dict(data, cache)
    elif data.is_list:
        ret = fill_cache_list(data, cache)
    elif data.source.is_extended:
        ret = {"inherited": 1, "not_inherited": 0}
    else:
        ret = {"inherited": 0, "not_inherited": 1}
    cache[id(data)] = ret
    return ret


def fill_cache_list(data, cache):
    # do not count this object as it is only a wrapper
    inherited = 0
    not_inherited = 0

    for item in data:
        rec = fill_cache(item, cache)
        inherited += rec["inherited"]
        not_inherited += rec["not_inherited"]

    return {"inherited": inherited, "not_inherited": not_inherited}


def fill_cache_dict(data, cache):
    # do not count this object as it is only a wrapper
    inherited = 0
    not_inherited = 0
    for item in data.value.values():
        rec = fill_cache(item, cache)
        inherited += rec["inherited"]
        not_inherited += rec["not_inherited"]

    return {"inherited": inherited, "not_inherited": not_inherited}


def find_extend_roots(data: SchemaValue):
    extended_elements = list(find_extended_elements(data))
    if not extended_elements:
        return
    parents = set(x.parent for x in extended_elements)
    parents = [x for x in parents if not any(y in x.ancestors for y in parents)]
    return parents


def find_extended_elements(data: SchemaValue):
    if data.source.is_extended:
        yield data
    elif data.is_list:
        for item in data:
            yield from find_extended_elements(item)
    elif data.is_dict:
        for value in data.value.values():
            yield from find_extended_elements(value)


def extract_extended_record(included_data, *, context, **kwargs):
    """
    This function extracts the record to be extended. The extended part is always object
        * If it is passed the whole model file, that is, "record" is inside, return that element
        * If there are 'properties' inside, return the whole object
        * As a fallback, return the whole object

    In all cases, it will strip everything apart from "type" and "properties"
    and keep those in "other_properties" inside the context so that other processors
    can add some of those selectively.
    """
    if (
        "record" in included_data
        and "properties" in included_data["record"]
        and "properties" not in included_data
    ):
        extended_object = included_data["record"]
    elif "properties" in included_data:
        extended_object = included_data
    else:
        context["props"] = included_data
        # need to return shallow copy, as there might be a manipulation with the
        # element and context would be corrupted
        return {**included_data}

    context["props"] = extended_object
    return {
        "properties": extended_object.get("properties", {}),
    }
