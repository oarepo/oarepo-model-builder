def convert_to_absolute_class_name(class_name, package_name):
    if "." not in class_name:
        return f"{package_name}.{class_name}"
    if class_name.startswith("."):
        package_path = package_name.split(".")
        while class_name.startswith("."):
            if package_path:
                package_path = package_path[:-1]
            class_name = class_name[1:]
        if package_path:
            class_name = f"{'.'.join(package_path)}.{class_name}"
    return class_name
