from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.python_name import package_name


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
    if "record" in included_data:
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


def extend_modify_marshmallow(included_data, *, context, **kwargs):
    """
    This processor modified marshmallow of the extended object. At first, it puts
    marshmallow and ui back to the included data. Then, for the top-level marshmallow & ui.marshmallow
    it converts class -> base-classes and adds import for that.
    For the properties, it marks them as read=False and write=False and for each object, it marks it as
    generate=False - this way, the classes will be reused from the already existing library and not
    generated again.
    """

    def remove_marshmallow_from_children(node):
        ret = {**node}
        node_properties = ret.pop("properties", None)
        node_items = ret.pop("items", None)
        ret["from-base-class"] = True

        if node_properties:
            properties = ret.setdefault("properties", {})
            for k, v in node_properties.items():
                remove_marshmallow_from_child(v)
                v = remove_marshmallow_from_children(v)
                properties[k] = v
        if node_items:
            remove_marshmallow_from_child(node.item)
            ret["items"] = remove_marshmallow_from_children(node.item)
        ret["base-class-marshmallow"] = ret.pop("marshmallow", {})
        ret["base-class-ui-marshmallow"] = ret.setdefault("ui", {}).pop(
            "marshmallow", {}
        )
        return ret

    def remove_marshmallow_from_child(child):
        # for object/nested, do not set the read & write to False because
        # the extending schema might add more properties.
        # This will generate unnecessary classes, but these might be dealt
        # on later in marshmallow generator
        if "properties" not in child and "items" not in child:
            marshmallow = child.setdefault("marshmallow", {})
            marshmallow.update({"read": False, "write": False})

            ui_marshmallow = child.setdefault("ui", {}).setdefault("marshmallow", {})
            ui_marshmallow.update({"read": False, "write": False})
        elif "properties" in child:
            # if there are properties, mark the object to not generate the class
            marshmallow = child.setdefault("marshmallow", {})
            marshmallow.update({"generate": False})

            ui_marshmallow = child.setdefault("ui", {}).setdefault("marshmallow", {})
            ui_marshmallow.update({"generate": False})

    def convert_marshmallow_class_to_base_class(marshmallow):
        # pop module & package
        marshmallow.pop("module", None)
        marshmallow.pop("package", None)

        if "class" not in marshmallow:
            return
        clz = marshmallow.pop("class")
        marshmallow.setdefault("base-classes", []).insert(0, clz)
        marshmallow.setdefault("imports", []).append(
            {"import": package_name(clz), "alias": package_name(clz)}
        )

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
    ret = remove_marshmallow_from_children(included_data, True)

    for ext in (
        ModelSchema.EXTEND_KEYWORD,
        ModelSchema.REF_KEYWORD,
        ModelSchema.USE_KEYWORD,
    ):
        if ext in context["props"]:
            ret[ext] = context["props"][ext]

    replace_use_with_extend(ret)
    return ret


def post_extend_modify_marshmallow(*, element, context, **kwargs):
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
                return

            is_object = "properties" in node
            if not is_object:
                new_marshmallow.update(base_marshmallow)
                return

            convert_to_base_classes = (
                node_properties and not contains_only_inherited_properties
            )
            if "class" in new_marshmallow:
                # someone added class to the new_marshmallow, so we do not want to change it
                convert_to_base_classes = True

            if convert_to_base_classes:
                if "class" in base_marshmallow:
                    new_marshmallow.setdefault("base-classes", []).insert(
                        0, base_marshmallow["class"]
                    )
                new_marshmallow["generate"] = True

            elif contains_only_inherited_properties:
                new_marshmallow.update(base_marshmallow)
                new_marshmallow["generate"] = False

            else:
                new_marshmallow.update(base_marshmallow)

        update_marshmallow(node.setdefault("marshmallow", {}), base_class_marshmallow)
        update_marshmallow(
            node.setdefault("ui", {}).setdefault("marshmallow", {}),
            base_class_ui_marshmallow,
        )

        return contains_only_inherited_properties

    convert_schema_classes(element)
