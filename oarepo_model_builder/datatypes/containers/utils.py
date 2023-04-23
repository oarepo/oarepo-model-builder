def deep_searchable_enabled(dt):
    if dt.definition.get("facets", {}).get("searchable", None) is False:
        return False
    children = getattr(dt, "children", {}).values()
    item = getattr(dt, "item", None)
    if item:
        return deep_searchable_enabled(item)
    for c in children:
        if not deep_searchable_enabled(c):
            return False
    return True
