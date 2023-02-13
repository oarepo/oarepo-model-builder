import re
import keyword


def convert_name_to_python(name):
    # special case :)

    name = name.replace("@v", "_version")
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


def convert_name_to_python_class(name):
    # Replace any spaces or special characters in the string with an underscore
    class_name = re.sub(r"[^\w\s]", "", name)
    class_name = re.sub(r"\s+", "_", class_name)

    # Capitalize the first letter of each word to form a nicely looking class name
    class_name = "".join([word.capitalize() for word in class_name.split("_")])

    return class_name
