def searchable(definition, create):
    if create:
        if definition != {}:
            if "searchable" in definition and not definition["searchable"]:
                return False
            else:
                return True
        else:
            return True
    else:
        if definition != {}:
            if "searchable" in definition and definition["searchable"]:
                return True
            elif "field" in definition or "key" in definition:
                return True
            else:
                return False
        else:
            return False
