from pathlib import Path
from typing import Callable, Dict

from oarepo_model_builder.schema.loader import SchemaLoader
from oarepo_model_builder.schema.value import Source
from oarepo_model_builder.validation import validate_model


class ModelSchema:
    USE_KEYWORD = "use"
    REF_KEYWORD = "$ref"
    EXTEND_KEYWORD = "extend"

    def __init__(
        self,
        file_path,
        content=None,
        included_models: Dict[str, Callable] = None,
        loaders=None,
        validate=True,
        schema_preprocessors=None,
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
        self._schema_preprocessors = schema_preprocessors or []

        self.loader = SchemaLoader(self.loaders, self.included_schemas)
        raw_schema = self.loader.load(Source.create(file_path, content=content))

        for preprocessor in self._schema_preprocessors:
            preprocessor(data=raw_schema, schema=self, loader=self.loader)

        self.schema = raw_schema.dump()

        self.schema.setdefault("settings", {})

        self._sections = {}

        self._strip_ignored_elements()

        if validate:
            validate_model(self)

    @property
    def settings(self):
        return self.schema.get("settings", {})

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

    def _strip_ignored_elements(self):
        extension_elements = self.schema.get("settings", {}).get(
            "extension-elements", []
        )
        extension_elements = [
            *extension_elements,
            *[f"^{x}" for x in extension_elements],
        ]
        if not extension_elements:
            return

        def remove_extension_elements(d):
            if isinstance(d, dict):
                for k, v in list(d.items()):
                    if k in extension_elements:
                        del d[k]
                    elif isinstance(v, (dict, list)):
                        remove_extension_elements(v)
            elif isinstance(d, list):
                for v in d:
                    if isinstance(v, (dict, list)):
                        remove_extension_elements(v)

        remove_extension_elements(self.schema)
