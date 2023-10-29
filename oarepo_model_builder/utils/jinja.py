import re

from jinja2 import pass_context

from .python_name import (  # noqa
    Import,
    PythonQualifiedName,
    base_name,
    package_name,
    split_base_name,
    split_package_base_name,
    split_package_name,
)


def sorted_imports(imports):
    # make the entries unique
    imports_dict = {(x["import"], x.get("alias")): x for x in imports}
    imports = list(imports_dict.values())
    # sort them

    imports.sort(key=lambda x: (x["import"], x.get("alias") or ""))
    return imports


def to_import_list(import_object, alias=None, base_classes_name="base-classes"):
    if isinstance(import_object, Import):
        return [{"import": import_object.import_path, "alias": import_object.alias}]
    elif isinstance(import_object, str):
        pn = PythonQualifiedName(import_object)
        if "." in pn.qualified_name:
            return to_import_list(pn.imports)
        else:
            return []
    elif isinstance(import_object, (tuple, list)):
        return [y for x in import_object for y in to_import_list(x)]
    elif isinstance(import_object, dict):
        ret = []
        if "import" in import_object:
            return [import_object]
        if "imports" in import_object:
            ret.extend(to_import_list(import_object["imports"]))
        if base_classes_name in import_object:
            ret.extend(to_import_list(import_object[base_classes_name]))
        if "extra-code" in import_object:
            ret.extend(
                to_import_list(extract_extra_code_imports(import_object["extra-code"]))
            )
        return ret
    return [import_object]


@pass_context
def generate_import(
    ctx, import_object, alias=None, skip=False, base_classes_name="base-classes"
):
    if skip:
        return ""
    import_list = to_import_list(
        import_object, alias=alias, base_classes_name=base_classes_name
    )
    return "\n".join(
        [generate_import_string(ctx, x) for x in sorted_imports(import_list)]
    )


def extract_extra_code_imports(extra_code):
    extra_code = (extra_code or "").strip()
    ret = []
    for match in re.finditer(r"{{(.*?)}}", extra_code):
        ret.extend(PythonQualifiedName(match.groups()[0]).imports)
    return ret


@pass_context
def generate_extra_code_imports(ctx, extra_code):
    return generate_import(ctx, extract_extra_code_imports(extra_code))


def generate_extra_code(obj, skip=False):
    if isinstance(obj, dict):
        extra_code = obj.get("extra-code", "")
    else:
        extra_code = obj
    extra_code = (extra_code or "").strip()
    if skip or not extra_code:
        return ""

    def replace_classes(matchobj):
        return PythonQualifiedName(matchobj.group(1)).local_name

    return re.sub(r"{{(.*?)}}", replace_classes, extra_code)


def generate_import_string(ctx, import_object):
    import_name = import_object["import"]
    alias = import_object.get("alias")
    ret = []

    if import_name == alias:
        # if import is the same as alias, keep just the import statement
        ret.append(f"import {import_name}")
    else:
        # otherwise break the import to path and base name and alias if defined
        if "." in import_name:
            import_path, import_name = import_name.rsplit(".", maxsplit=1)
        else:
            import_path = None
        if import_path:
            if ctx["current_module"] == import_path:
                return ""  # do not import from the same module
            ret.append(f"from {import_path} import {import_name}")
        else:
            ret.append(f"import {import_name}")
        if alias and alias != import_name:
            ret.append(f"as {alias}")
    return " ".join(ret)


def generate_list(data, separator=", ", start=False, end=False):
    if not data:
        return ""
    ret = []
    if start:
        ret.append(separator)
    for di, d in enumerate(data):
        if di:
            ret.append(separator)
        ret.append(generate_extra_code(d))
    if end:
        ret.append(separator)
    return "".join(ret)


def in_different_package(current_module, value):
    return current_module != package_name(value)


def with_defined_prefix(always_defined_import_prefixes, value):
    return package_name(value) in always_defined_import_prefixes


def class_header(rec, class_name="class", base_classes_name="base-classes"):
    try:
        ret = [
            base_name(rec[class_name]),
        ]
    except KeyError:
        raise KeyError(f'Do not have "{class_name}" inside {rec}')
    base_classes = rec[base_classes_name]
    if base_classes:
        ret.append("(")
        for idx, cls in enumerate(base_classes):
            pn = PythonQualifiedName(cls)
            if idx > 0:
                ret.append(", ")
            ret.append(pn.local_name)
        ret.append(")")
    return "".join(ret)
