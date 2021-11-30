import copy
import pathlib
from typing import Dict, Callable

import munch
from jsonpointer import resolve_pointer

from .exceptions import IncludedFileNotFoundException
from .utils.deepmerge import deepmerge
from .utils.hyphen_munch import HyphenMunch


class ModelSchema:
    OAREPO_USE = 'oarepo:use'

    def __init__(self, file_path, content=None,
                 included_models: Dict[str, Callable] = None,
                 loaders=None):
        """
        Creates and parses model schema

        :param file_path: path on the filesystem to the model schema file
        :param content:   if set, use this content, otherwise load the file_path
        :param included_models: a dictionary of file_id to callable that returns included json.
                The callable expects a single parameter, an instance of this schema
        """

        self.file_path = file_path
        self.included_schemas = included_models or {}
        self.loaders = loaders

        if content is not None:
            self.schema = content
        else:
            self.schema = copy.deepcopy(self._load(file_path))

        self._resolve_references(self.schema, [])

        self.schema.setdefault('settings', {})
        self.schema['settings'].setdefault('plugins', {})
        self.schema = munch.munchify(self.schema, factory=HyphenMunch)

    def get(self, key):
        return self.schema.get(key, None)

    def set(self, key, value):
        self.schema[key] = value

    @property
    def settings(self):
        return self.schema.settings

    def merge(self, another):
        self.schema = munch.munchify(deepmerge(another, self.schema, []), factory=HyphenMunch)

    def _load(self, file_path):
        """
        Loads a json/json5 file on the path

        :param file_path: file path on filesystem
        :return: parsed json
        """
        extension = pathlib.Path(file_path).suffix.lower()[1:]
        if extension in self.loaders:
            return self.loaders[extension](file_path, self)

        raise Exception(f'Can not load {file_path} - no loader has been found for extension {extension} '
                        f'in entry point group oarepo_model_builder.loaders')

    def _load_included_file(self, file_id):
        """
        Resolve and load an included file. Internal method called when loading schema.
        If the included file contains a json pointer,
        return only the part identified by the json pointer.

        :param file_id: the id of the included file, might contain #xpointer
        :return:    loaded json
        """
        if '#' in file_id:
            file_id, json_pointer = file_id.rsplit('#', 1)
        else:
            json_pointer = None

        if file_id not in self.included_schemas:
            raise IncludedFileNotFoundException(f'Included file {file_id} not found in includes')

        ret = self.included_schemas[file_id](self)

        if json_pointer:
            ret = resolve_pointer(ret, json_pointer)

        return copy.deepcopy(ret)

    def _resolve_references(self, element, stack):
        if isinstance(element, dict):
            if self.OAREPO_USE in element:
                included_name = element.pop(self.OAREPO_USE)
                included_data = self._load_included_file(included_name)
                deepmerge(element, included_data, [])
                return self._resolve_references(element, stack)
            for k, v in element.items():
                self._resolve_references(v, stack + [k])
        elif isinstance(element, list):
            for v in element:
                self._resolve_references(v, stack)


