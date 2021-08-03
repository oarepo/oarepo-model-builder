import os
from collections import namedtuple

from oarepo_model_builder.outputs import BaseOutput

from tomlkit import parse, dumps, document, table

toml_property = namedtuple('toml_property', 'section, property, value')


class TomlOutput(BaseOutput):
    """Output that handles JSON formatted data."""

    def __init__(self, path):
        super().__init__(path)
        self.props_to_add = []
        self.props_to_remove = []

    def add(self, section, property, value):
        self.props_to_add.append(toml_property(section, property, value))

    def remove(self, section, property, value):
        self.props_to_remove.append(toml_property(section, property, value))

    def save(self):
        if os.path.exists(self.path):
            with open(self.path, mode='r') as fp:
                toml = parse(fp.read())
        else:
            toml = document()

        for prop in self.props_to_add:
            if prop.section not in toml:
                section = table()
                toml.add(prop.section, section)
            else:
                section = toml[prop.section]
            section[prop.property] = prop.value

        for prop in self.props_to_remove:
            if prop.section not in toml:
                continue
            else:
                section = toml[prop.section]
            if prop.property in section:
                del section[prop.property]

        with open(self.path, mode='w') as fp:
            fp.write(dumps(toml))
