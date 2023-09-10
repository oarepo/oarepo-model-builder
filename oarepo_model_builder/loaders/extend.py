from oarepo_model_builder.utils.python_name import package_name
from oarepo_model_builder.validation import InvalidModelException


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
        raise InvalidModelException("Extended object must be an object")

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

        if "marshmallow" not in ret:
            raise InvalidModelException(
                f"marshmallow section not in {node}. "
                f"Please pass generated model (records.json5), not the source model."
            )
        if "ui" not in ret or "marshmallow" not in ret["ui"]:
            raise InvalidModelException(
                f"ui.marshmallow section not in {node}. "
                f"Please pass generated model (records.json5), not the source model."
            )

        convert_marshmallow_class_to_base_class(ret["marshmallow"])
        convert_marshmallow_class_to_base_class(ret["ui"]["marshmallow"])

        if node_properties:
            properties = ret.setdefault("properties", {})
            for k, v in node_properties.items():
                remove_marshmallow_from_child(v)
                v = remove_marshmallow_from_children(v)
                properties[k] = v
        if node_items:
            remove_marshmallow_from_child(node.item)
            ret["items"] = remove_marshmallow_from_children(node.item)
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

    included_data["marshmallow"] = context["props"].get("marshmallow", {})
    included_data["ui"] = context["props"].get("ui", {})
    ret = remove_marshmallow_from_children(included_data)
    import yaml

    with open("/tmp/test.yaml", "w") as f:
        yaml.safe_dump(ret, f)
    return ret
