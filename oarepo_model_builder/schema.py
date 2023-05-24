import copy
import os
import pathlib
from pathlib import Path
from typing import Callable, Dict, List, Union

from jsonpointer import resolve_pointer

from .exceptions import IncludedFileNotFoundException
from .utils.deepmerge import deepmerge
from .validation import validate_model


class ModelSchema:
    USE_KEYWORD = "use"
    REF_KEYWORD = "$ref"

    def __init__(
        self,
        file_path,
        content=None,
        included_models: Dict[str, Callable] = None,
        merged_models: List[Union[str, Path]] = None,
        loaders=None,
        validate=True,
        source_locations=None,
    ):
        """
        Creates and parses model schema

        :param file_paths: list of paths on the filesystem to the model schema files. The content of these files will be merged before the processing.
        :param content:   if set, use this content, otherwise load the file_path
        :param included_models: a dictionary of file_id to callable that returns included json.
                The callable expects a single parameter, an instance of this schema
        """

        self.file_path = file_path
        self.included_schemas = included_models or {}
        self.loaders = loaders
        self.source_locations = [*(source_locations or [])]
        self.source_locations.append(os.path.abspath(os.curdir))
        self.source_locations.append(os.path.dirname(os.path.abspath(self.file_path)))

        if content is not None:
            self.schema = content
        else:
            self.schema = copy.deepcopy(self._load(file_path))
            for fp in merged_models or []:
                self.schema = deepmerge(self.schema, copy.deepcopy(self._load(fp)))

        self._resolve_references(self.schema, [])

        self._resolve_shortcuts(self.schema)

        # any star keys should be kept
        use_star_keys(self.schema)

        self.schema.setdefault("settings", {})

        self._sections = {}

        if validate:
            validate_model(self)

    @property
    def settings(self):
        return self.schema.get("settings", {})

    def _load(self, file_path, content=None):
        """
        Loads a json/json5 file on the path

        :param file_path: file path on filesystem
        :return: parsed json
        """
        if file_path in self.included_schemas:
            loaded = self._fetch_included(file_path)
        else:
            extension = pathlib.Path(file_path).suffix.lower()[1:]
            if extension not in self.loaders:
                raise RuntimeError(
                    f"Can not load {file_path} - no loader has been found for extension {extension} "
                    f"in entry point group oarepo_model_builder.loaders"
                )
            loaded = self.loaders[extension](file_path, self, content=content)
        return loaded

    def _fetch_included(self, file_path):
        included = self.included_schemas[file_path]
        if callable(included):
            return included(self)
        extension = pathlib.Path(included).suffix.lower()[1:]
        if extension not in self.loaders:
            raise RuntimeError(
                f"Can not load {included} - no loader has been found for extension {extension} "
                f"in entry point group oarepo_model_builder.loaders"
            )
        return self.loaders[extension](included, self)

    def _load_included_file(self, location, source_locations=None):
        """
        Resolve and load an included file. Internal method called when loading schema.
        If the included file contains a json pointer,
        return only the part identified by the json pointer.

        :param file_id: the id of the included file, might contain #xpointer
        :return:    loaded json
        """
        if "#" in location:
            file_id, json_pointer_or_id = location.rsplit("#", 1)
        else:
            file_id = location
            json_pointer_or_id = None

        if not file_id or file_id == ".":
            ret = self.schema
        else:
            file_path = self._resolve_file_path(file_id, source_locations)
            if file_path:
                # relative include
                ret = self._load(file_path)
            else:
                if file_id not in self.included_schemas:
                    raise IncludedFileNotFoundException(
                        f"Included file {file_id} not found in includes"
                    )

                ret = self._fetch_included(file_id)

        if json_pointer_or_id:
            if json_pointer_or_id.startswith("/"):
                ret = resolve_pointer(ret, json_pointer_or_id)
            else:
                ret = resolve_id(ret, json_pointer_or_id)
                if not ret:
                    raise IncludedFileNotFoundException(
                        f"Element with id {json_pointer_or_id} not found in {file_id}"
                    )

        ret = copy.deepcopy(ret)
        if ret is None:
            ret = {}
        ret.pop("$id", None)
        return ret

    def _resolve_file_path(self, file_id, source_locations):
        if file_id in self.included_schemas:
            return file_id
        source_locations = [*(source_locations or []), *self.source_locations]
        for location in source_locations:
            pth = Path(location) / file_id
            if pth.exists():
                return pth
        pth = self.abs_path.parent / file_id
        if pth.exists():
            return pth
        return None

    def _resolve_shortcuts(self, element):
        if isinstance(element, dict):
            for v in element.values():
                self._resolve_shortcuts(v)
        elif isinstance(element, list):
            for v in element:
                self._resolve_shortcuts(v)

    def _resolve_references(self, element, stack):
        if isinstance(element, dict):
            if self.USE_KEYWORD in element or self.REF_KEYWORD in element:
                for key in element:
                    if key in (self.USE_KEYWORD, self.REF_KEYWORD):
                        break
                included_name = element[key]

                # if it is a dictionary, then probably it is a name of a property,
                # so keep it
                if isinstance(included_name, dict):
                    return self._resolve_references(element, stack)

                element.pop(self.USE_KEYWORD, None)
                element.pop(self.REF_KEYWORD, None)

                if not isinstance(included_name, list):
                    included_name = [included_name]
                for name in included_name:
                    if not name:
                        raise IncludedFileNotFoundException(
                            f"No file for use at path {'/'.join(stack)}"
                        )
                    included_data = self._load_included_file(name)
                    deepmerge(element, included_data, [], listmerge="keep")
                return self._resolve_references(element, stack)
            for k, v in element.items():
                self._resolve_references(v, stack + [k])
        elif isinstance(element, list):
            for v in element:
                self._resolve_references(v, stack)

    @property
    def abs_path(self):
        return Path(self.file_path).absolute()

    def get_schema_section(self, profile, section, prepare_context=None):
        if not isinstance(section, (tuple, list)):
            section = (section,)
        section = tuple(section)
        key = (profile, section)
        if key in self._sections:
            return self._sections[key]
        from oarepo_model_builder.datatypes import datatypes

        data = self.schema
        for p in section:
            if p in data:
                data = data[p]
            else:
                data = {}
                break
        if "type" not in data:
            data["type"] = "model"
        parsed_section = datatypes.get_datatype(
            parent=None,
            data=data,
            key=None,
            model=data,
            schema=self,
        )
        prepare_context = prepare_context or {}
        prepare_context.setdefault("profile", profile)
        prepare_context.setdefault("profile_module", profile + "s")
        prepare_context.setdefault("profile_upper", profile.upper())
        parsed_section.prepare(prepare_context)
        self._sections[key] = parsed_section
        return parsed_section


def resolve_id(json, element_id):
    if isinstance(json, dict):
        if "$id" in json and json["$id"] == element_id:
            return json
        continue_with = json.values()
    elif isinstance(json, (tuple, list)):
        continue_with = json
    else:
        return None
    for k in continue_with:
        ret = resolve_id(k, element_id)
        if ret is not None:
            return ret


def remove_star_keys(schema):
    if isinstance(schema, dict):
        for k, v in list(schema.items()):
            if k.startswith("*"):
                del schema[k]
            else:
                remove_star_keys(v)
    elif isinstance(schema, (list, tuple)):
        for k in schema:
            remove_star_keys(k)


def use_star_keys(schema):
    if isinstance(schema, dict):
        for k, v in list(schema.items()):
            if k.startswith("*"):
                del schema[k]
                schema[k[1:]] = v
        for v in schema.values():
            use_star_keys(v)
    elif isinstance(schema, (list, tuple)):
        for k in schema:
            use_star_keys(k)
