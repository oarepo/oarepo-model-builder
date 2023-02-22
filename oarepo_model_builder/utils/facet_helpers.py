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
            if "searchable" in definition and not definition["searchable"]:
                return False
            else:
                return True
        else:
            return False
