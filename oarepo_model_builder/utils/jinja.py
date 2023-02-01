def package_name(value):
    return value.rsplit(".", maxsplit=1)[0]


def split_package_name(value):
    return package_name(value)


def base_name(value):
    return value.rsplit(".", maxsplit=1)[-1]


def split_base_name(value):
    return base_name(value)


def split_package_base_name(value):
    if "." not in value:
        return None, value
    return value.rsplit(".", maxsplit=1)


def in_different_package(current_package_name, value):
    return current_package_name != package_name(value)


def with_defined_prefix(always_defined_import_prefixes, value):
    return package_name(value) in always_defined_import_prefixes
