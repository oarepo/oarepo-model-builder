import importlib


def import_class(signature):
    package_name, class_name = signature.split(":")
    return getattr(importlib.import_module(package_name), class_name)
