from .python_name import (  # noqa
    base_name,
    package_name,
    split_base_name,
    split_package_base_name,
    split_package_name,
)


def sorted_imports(imports):
    imports = list(sorted(imports, key=lambda x: (x["import"], x.get("alias"))))
    return imports


def in_different_package(current_package_name, value):
    return current_package_name != package_name(value)


def with_defined_prefix(always_defined_import_prefixes, value):
    return package_name(value) in always_defined_import_prefixes
