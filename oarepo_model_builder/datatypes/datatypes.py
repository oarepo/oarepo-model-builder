import copy
import dataclasses
import json
from collections.abc import Mapping
from functools import cached_property, lru_cache
from typing import Any, Dict, List, Optional, Type, Union

import importlib_metadata
import marshmallow as ma
from marshmallow import fields

from ..utils.deepmerge import deepmerge
from ..utils.import_class import import_class
from ..utils.properties import class_property
from ..validation.utils import PermissiveSchema


@dataclasses.dataclass
class Import:
    import_path: str
    alias: Optional[str] = None

    @staticmethod
    def from_config(d):
        if isinstance(d, dict):
            return Import(d["import"], d.get("alias"))
        elif isinstance(d, (tuple, list)):
            return [Import.from_config(x) for x in d]

    def __hash__(self):
        return hash(self.import_path) ^ hash(self.alias)

    def __eq__(self, o):
        return self.import_path == o.import_path and self.alias == o.alias


@dataclasses.dataclass
class Section:
    section_name: str
    config: Dict[str, Any]
    children: Dict[str, "AbstractDataType"] = dataclasses.field(default_factory=dict)
    item: "AbstractDataType" = None

    @cached_property
    def fingerprint(self):
        f = [self.section_name, json.dumps(self.config, sort_keys=True, default=repr)]
        for key, dt in self.children.items():
            f.append(f"  @@@ {key} {type(dt).__name__}")
            f.append(
                "    "
                + getattr(dt, "section_" + self.section_name).fingerprint.replace(
                    "\n", "\n    "
                )
            )
        if self.item:
            f.append(f"### {type(self.item).__name__}")
            f.append(
                getattr(self.item, "section_" + self.section_name).fingerprint.replace(
                    "\n", "\n  "
                )
            )
        return "\n".join(f)


class MergedAttrDict(Mapping):
    def __init__(self, source, fallback):
        self._source = source
        self._fallback = fallback

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        if key in self._source:
            return self._source[key]
        return self._fallback[key]

    def __getattr__(self, key):
        try:
            return self[key.replace("_", "-")]
        except KeyError:
            raise AttributeError(f"Attribute {key} not found")

    def __len__(self):
        return len(self.keys())

    def keys(self):
        return set(self._source.keys()).union(self._fallback.keys())


class AbstractDataType:
    parent: "AbstractDataType"
    children: Dict[str, "AbstractDataType"]

    def __init__(
        self,
        parent: "AbstractDataType",
        definition: Any,
        key: str,
        model: Any,
        schema: Any,
    ):
        self.parent = parent
        self.children = {}
        self.definition = definition
        self.key = key
        self.model = model
        self.schema = schema
        self._sections = {}

    def copy(self, without_children=False):
        ret = type(self)(
            # shallow copy of the definition to enable overwriting pieces of it
            self.parent,
            {**self.definition},
            self.key,
            self.model,
            self.schema,
        )
        ret.__dict__.update(
            {
                k: v
                for k, v in self.__dict__.items()
                if k
                not in (
                    "parent",
                    "definition",
                    "key",
                    "model",
                    "schema",
                    "_sections",
                    "children",
                    "item",
                )
            }
        )
        # clear up sections
        ret._sections = {}
        if without_children:
            if ret.children:
                ret.children = {}
            elif hasattr(ret, "item"):
                ret.item = None
        return ret

    def prepare(self, context):
        """
        Prepare the datatype. This might fill "children" property as well
        """

    def __getattr__(self, name):
        """
        datatype.json_schema maps to self.definition['json-schema'].
        If it has not been found, an empty section is returned.

        At first _process_json_schema is called on the datatype, if it exists.

        Before returning, process_json_schema method is called on all components (datatypes.components)
        with datatype and section keyword arguments
        """
        if name.startswith("section_"):
            name = name[len("section_") :]
            run_processors = True
        elif name.startswith("default_section_"):
            name = name[len("default_section_") :]
            run_processors = False
        else:
            config_key = name.replace("_", "-")
            if config_key in self.definition:
                return self.definition[config_key]

            return object.__getattribute__(self, name)

        # get the section
        section_key = name.replace("_", "-")
        if section_key in self._sections:
            return self._sections[section_key]
        config = self.definition.get(section_key, {})
        config = copy.deepcopy(config)

        # get the default from datatype
        if hasattr(self, name):
            deepmerge(config, copy.deepcopy(getattr(self, name)))

        section = Section(
            name, config, getattr(self, "children", {}), getattr(self, "item", None)
        )

        if run_processors:
            if hasattr(self, f"_process_{name}"):
                getattr(self, f"_process_{name}")(section=section)

            # call components
            datatypes.call_components(
                self,
                f"process_{name}",
                section=section,
            )
        self._sections[section_key] = section
        return section

    @cached_property
    def path(self):
        ret = []
        p = self
        while p:
            if p.key:
                ret.append(p.key)
            p = p.parent
        return ".".join(reversed(ret))

    @cached_property
    def stack(self):
        ret = []
        p = self
        while p:
            ret.append(p)
            p = p.parent
        return tuple(reversed(ret))


class DataType(AbstractDataType):
    model_type = None

    class ModelSchema(ma.Schema):
        type = fields.String(required=True)
        required = fields.Bool()
        jsonschema = fields.Nested(PermissiveSchema)
        mapping = fields.Nested(PermissiveSchema)
        id = fields.String(
            metadata={
                "doc": "Optional id of this element (for example, for referencing the element)"
            }
        )

    def prepare(self, context):
        self.id = self.definition.get("id")
        datatypes.call_components(datatype=self, method="prepare", context=context)

    @class_property
    def validator(cls):
        validators = list(
            datatypes.call_class_components(datatype=cls, method="model_schema")
        ) + list(datatypes.get_class_components(cls, "ModelSchema"))
        validators = [x for x in validators if x]
        unique_validators = []
        for v in validators:
            if v not in unique_validators:
                unique_validators.append(v)

        class Meta:
            unknown = ma.RAISE

        ret = type(
            f"{cls.__name__}ModelValidator",
            (*unique_validators, cls.ModelSchema),
            {"Meta": Meta},
        )
        return ret

    def deep_iter(self):
        yield self

    def _process_json_schema(self, section: Section, **__kwargs):
        section.config.setdefault("type", self.definition["type"])

    def _process_mapping(self, section: Section, **__kwargs):
        section.config.setdefault("type", self.definition["type"])


class DataTypeComponent:
    eligible_datatypes = []


class DataTypes:
    @cached_property
    def datatype_map(self) -> Dict[str, DataType]:
        d = {}
        for entry in importlib_metadata.entry_points(
            group="oarepo_model_builder.datatypes"
        ):
            for dt in entry.load():
                d[dt.model_type] = dt
        return d

    @cached_property
    def components(self) -> List[DataTypeComponent]:
        c = []
        for entry in importlib_metadata.entry_points(
            group="oarepo_model_builder.datatypes.components"
        ):
            for component in entry.load():
                c.append(component())
        return c

    @lru_cache(maxsize=1024)
    def _get_components(self, datatype_class):
        datatype_components = []

        for component in self.components:
            if not component.eligible_datatypes:
                datatype_components.append(component)
            else:
                for depends_on in component.eligible_datatypes:
                    if isinstance(depends_on, str):
                        depends_on = import_class(depends_on)
                    if issubclass(datatype_class, depends_on):
                        datatype_components.append(component)
                        break

        # remove overridden components
        unsorted_components = []
        non_leaf_components = set()
        for c in datatype_components:
            non_leaf_components.update(type(c).mro()[1:])

        for c in datatype_components:
            if type(c) not in non_leaf_components:
                unsorted_components.append(c)

        dependency_remaps = {}
        for c in unsorted_components:
            remap = getattr(c, "dependency_remap", None)
            if remap:
                dependency_remaps[remap] = type(c)
        # sort by dependencies
        depsort_map = {}

        def get_dependent_component(component):
            return (
                dependency_remaps[component]
                if component in dependency_remaps
                else component
            )

        for c in unsorted_components:
            dependencies_classes = depsort_map.setdefault(type(c), [])
            depsort_map[type(c)] = dependencies_classes
            for depends_on in getattr(c, "depends_on", []):
                depends_on = get_dependent_component(depends_on)
                if isinstance(depends_on, str):
                    depends_on = import_class(depends_on)
                dependencies_classes.append(depends_on)
            for affects in getattr(c, "affects", []):
                affects = get_dependent_component(affects)
                if isinstance(affects, str):
                    affects = import_class(affects)
                depsort_map.setdefault(affects, []).append(type(c))

        sorted_components = []
        while unsorted_components:
            new_unsorted_components = []
            current_round_sorted_components = set()
            for c in unsorted_components:
                if not depsort_map[type(c)]:
                    sorted_components.append(c)
                    current_round_sorted_components.add(type(c))
                else:
                    new_unsorted_components.append(c)
            if len(new_unsorted_components) == len(unsorted_components):
                raise AttributeError(
                    f"A loop has been detected in component dependencies: {unsorted_components}"
                )
            for c in new_unsorted_components:
                depsort_map[type(c)] = [
                    x
                    for x in depsort_map[type(c)]
                    if x not in current_round_sorted_components
                ]
            unsorted_components = new_unsorted_components
        return tuple(sorted_components)

    def get_datatype(self, parent, data, key, model, schema) -> Union[DataType, None]:
        datatype_class = self.get_datatype_class(data.get("type", None))
        if datatype_class:
            return datatype_class(parent, data, key, model, schema)
        if parent:
            raise KeyError(
                f"Do not have datatype for the following data at path '{parent.path}':\n"
                f"{json.dumps(data, indent=4, ensure_ascii=False)}"
            )
        raise KeyError(
            f"Do not have datatype for the following data:\n"
            f"{json.dumps(data, indent=4, ensure_ascii=False)}"
        )

    def get_datatype_class(self, datatype_type):
        return self.datatype_map.get(datatype_type)

    def call_components(self, datatype: DataType, method: str, **kwargs):
        ret = []
        for component in self._get_components(type(datatype)):
            if hasattr(component, method):
                ret.append(getattr(component, method)(datatype=datatype, **kwargs))
        return ret

    def call_class_components(self, datatype: Type[DataType], method: str, **kwargs):
        ret = []
        for component in self._get_components(datatype):
            if hasattr(component, method):
                ret.append(getattr(component, method)(datatype=datatype, **kwargs))
        return ret

    def get_class_components(self, datatype: Type[DataType], name: str):
        ret = []
        for component in self._get_components(datatype):
            if hasattr(component, name):
                ret.append(getattr(component, name))
        return ret

    def _clear_caches(self):
        """
        mostly for testing
        """
        self._get_components.cache_clear()
        try:
            del self.datatype_map
        except:  # NOSONAR intentionally broad, used only in tests
            pass
        try:
            del self.components
        except:  # NOSONAR intentionally broad, used only in tests
            pass


datatypes = DataTypes()
