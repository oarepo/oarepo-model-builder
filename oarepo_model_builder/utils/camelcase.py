import re


def camel_case(s):
    s = re.split("_|-", s)
    s = [x[0].title() + x[1:] for x in s]
    return "".join(s)


def snake_case(s):
    s = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    s = re.sub("__([A-Z])", r"_\1", s)
    s = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()
