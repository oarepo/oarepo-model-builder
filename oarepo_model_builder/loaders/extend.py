from oarepo_model_builder.schema import ModelSchema


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

def add_record_to_included_data(included_data, *, context, **kwargs):
    if "props" in context and "record" in context["props"]:
        included_data["record"] = context["props"]["record"]
    return included_data


def extend_modify_marshmallow(included_data, *, context, **kwargs):
    """
    This processor moves the marshmallow section of the base record to base-class-marshmallow
    and base-class-ui-marshmallow. It also sets the from-base-class flag to True.
    """

    def mark_as_from_base_class(node):
        ret = {**node}
        node_properties = ret.pop("properties", None)
        node_items = ret.pop("items", None)
        ret["from-base-class"] = True

        if node_properties:
            properties = ret.setdefault("properties", {})
            for k, v in node_properties.items():
                v = mark_as_from_base_class(v)
                properties[k] = v
        if node_items:
            ret["items"] = mark_as_from_base_class(node.item)
        ret["base-class-marshmallow"] = ret.pop("marshmallow", {})
        ret["base-class-ui-marshmallow"] = ret.setdefault("ui", {}).pop(
            "marshmallow", {}
        )
        return ret

    def as_array(x):
        if isinstance(x, list):
            return x
        if not x:
            return []
        return [x]

    def replace_use_with_extend(data):
        if isinstance(data, dict):
            if ModelSchema.USE_KEYWORD in data:
                data.setdefault(ModelSchema.EXTEND_KEYWORD, []).extend(
                    as_array(data.pop(ModelSchema.USE_KEYWORD))
                )
            if ModelSchema.REF_KEYWORD in data:
                data.setdefault(ModelSchema.EXTEND_KEYWORD, []).extend(
                    as_array(data.pop(ModelSchema.REF_KEYWORD))
                )
            for v in data.values():
                if isinstance(v, (dict, list)):
                    replace_use_with_extend(v)
        elif isinstance(data, list):
            for v in data:
                if isinstance(v, (dict, list)):
                    replace_use_with_extend(v)

    included_data["marshmallow"] = context["props"].get("marshmallow", {})
    included_data["ui"] = context["props"].get("ui", {})
    ret = mark_as_from_base_class(included_data)

    for ext in (
        ModelSchema.EXTEND_KEYWORD,
        ModelSchema.REF_KEYWORD,
        ModelSchema.USE_KEYWORD,
    ):
        if ext in context["props"]:
            ret[ext] = context["props"][ext]

    replace_use_with_extend(ret)
    return ret


def post_extend_modify_marshmallow(*, element, **kwargs):
    def convert_schema_classes(node):
        node_properties = node.get("properties", None)
        node_items = node.get("items", None)

        was_inherited = "from-base-class" in node
        if not was_inherited:
            return False

        contains_only_inherited_properties = node.pop("from-base-class", False)
        if node_properties:
            for k, v in node_properties.items():
                prop_contains_only_inherited_properties = convert_schema_classes(v)
                if not prop_contains_only_inherited_properties:
                    contains_only_inherited_properties = False
        elif node_items:
            contains_only_inherited_properties = (
                convert_schema_classes(node_items)
                and contains_only_inherited_properties
            )
        base_class_marshmallow = node.pop("base-class-marshmallow", {})
        base_class_ui_marshmallow = node.pop("base-class-ui-marshmallow", {})

        def update_marshmallow(new_marshmallow, base_marshmallow):
            if new_marshmallow.get("generate", True) is False:
                # the class is set to not generate -> if there is a class, do not change it,
                # if not, set it to the base class
                if not new_marshmallow.get("class") and base_marshmallow.get("class"):
                    new_marshmallow["class"] = base_marshmallow["class"]
                return

            if "items" in node:
                # array itself does not have a marshmallow, so no need to modify this
                _update_non_existing(new_marshmallow, base_marshmallow)
                return

            if "properties" not in node:
                # primitive data type -> set it not to be generated unless the field says otherwise
                if "read" not in new_marshmallow:
                    new_marshmallow["read"] = False
                if "write" not in new_marshmallow:
                    new_marshmallow["write"] = False
                for k, v in base_marshmallow.items():
                    if k not in new_marshmallow:
                        new_marshmallow[k] = v
                return

            # now we have an object to modify - convert to base classes only if there are extra properties
            convert_to_base_classes = (
                node_properties and not contains_only_inherited_properties
            )

            if "class" in new_marshmallow:
                # someone added class to the new_marshmallow, so we do not want to change it
                convert_to_base_classes = True

            if convert_to_base_classes:
                if base_marshmallow.get("class"):
                    new_marshmallow["base-classes"] = [base_marshmallow["class"]]
                new_marshmallow["generate"] = True

            elif contains_only_inherited_properties:
                # keep the base class marshmallow, but do not generate the class as it has been generated
                # in the extended library
                new_marshmallow.clear()
                new_marshmallow.update(base_marshmallow)
                new_marshmallow["generate"] = False

            else:
                _update_non_existing(new_marshmallow, base_marshmallow)

        update_marshmallow(node.setdefault("marshmallow", {}), base_class_marshmallow)
        update_marshmallow(
            node.setdefault("ui", {}).setdefault("marshmallow", {}),
            base_class_ui_marshmallow,
        )

        return contains_only_inherited_properties

    convert_schema_classes(element)


def _update_non_existing(target, source):
    for k, v in source.items():
        if k not in target:
            target[k] = v
