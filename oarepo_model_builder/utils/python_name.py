import keyword
import re


def convert_name_to_python(name):
    # special case :)

    name = name.replace("@v", "_version")
    if name == "id":
        name = name.replace("id", "_id")
    # Replace any spaces or special characters in the string with an underscore
    identifier = re.sub(r"[^\w\s]", "_", name)
    identifier = re.sub(r"\s+", "_", identifier)

    # Ensure that the first character of the identifier is a letter or an underscore
    if identifier[0].isdigit():
        identifier = "_" + identifier

    # Ensure that the resulting identifier is not a reserved keyword in Python
    if keyword.iskeyword(identifier):
        identifier = identifier + "_"

    return identifier


def capitalize(s):
    return s[0].capitalize() + s[1:]


def convert_name_to_python_class(name):
    class_name = "".join([capitalize(word) for word in name.split("-")])
    class_name = "".join([capitalize(word) for word in class_name.split("_")])

    # Replace any spaces or special characters in the string with an underscore
    class_name = re.sub(r"[^\w\s]", "", class_name)
    class_name = re.sub(r"\s+", "_", class_name)

    return class_name
