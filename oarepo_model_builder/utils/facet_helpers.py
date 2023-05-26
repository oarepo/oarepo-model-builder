from .python_name import convert_name_to_python


def flatten(list_of_lists):
    return [x for l in list_of_lists for x in l]


def facet_definition(obj):
    key = None
    field = None
    args = None
    path = None
    if "facets" in obj.definition:
        facets = obj.definition["facets"]
        key = facets.get("key", obj.key)
        field = facets.get("field", None)
        args = facets.get("args", None)
        path = facets.get("path", None)
    if not key:
        key = obj.key
    return key, field, args, path


def facet_name(path):
    path.replace(".", "_")
    path = convert_name_to_python(path)
    return path
