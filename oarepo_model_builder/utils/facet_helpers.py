from .python_name import convert_name_to_python


def facet_definition(obj):
    key = None
    field = None
    if "facets" in obj.definition:
        key = obj.definition["facets"].get("key", obj.key)
        field = obj.definition["facets"].get("field", None)
    if not key:
        key = obj.key
    return key, field


def facet_name(path):
    path.replace(".", "_")
    path = convert_name_to_python(path)
    return path
