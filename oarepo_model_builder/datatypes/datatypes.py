import copy
import dataclasses
import json
from functools import cached_property, lru_cache
from typing import Any, Dict, List, Type, Union

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
    alias: str = None

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

    @property
    def child(self):
        assert len(self.children) == 1
        return next(iter(self.children.values()))

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

        # json schema
        json_schema = ma.fields.Nested(
            PermissiveSchema,
            attribute="json-schema",
            data_key="json-schema",
            required=False,
        )

        # mapping
        mapping = ma.fields.Nested(
            PermissiveSchema,
            attribute="mapping",
            data_key="mapping",
            required=False,
        )

    def prepare(self, context):
        datatypes.call_components(datatype=self, method="prepare", context=context)

    @class_property
    def validator(clz):
        validators = list(
            datatypes.call_class_components(datatype=clz, method="model_schema")
        ) + list(datatypes.get_class_components(clz, "ModelSchema"))
        validators = [x for x in validators if x]

        class Meta:
            unknown = ma.RAISE

        ret = type(
            f"{clz.__name__}ModelValidator",
            (*validators, clz.ModelSchema),
            {"Meta": Meta},
        )
        # print(clz)
        # print([x.__qualname__ for x in ret.mro()])
        # print([r for r in sorted(ret._declared_fields)])
        # print()
        return ret

    def deep_iter(self):
        yield self

    def _process_json_schema(self, section: Section, **kwargs):
        section.config.setdefault("type", self.definition["type"])

    def _process_mapping(self, section: Section, **kwargs):
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

    @lru_cache()
    def _get_components(self, datatype_class):
        datatype_components = []
        for component in self.components:
            if not component.eligible_datatypes:
                datatype_components.append(component)
            else:
                for dt in component.eligible_datatypes:
                    if isinstance(dt, str):
                        dt = import_class(dt)
                    if issubclass(datatype_class, dt):
                        datatype_components.append(component)
                        break
        # remove overridden components
        ret = []
        non_leaf_components = set()
        for c in datatype_components:
            non_leaf_components.update(type(c).mro()[1:])

        for c in datatype_components:
            if type(c) not in non_leaf_components:
                ret.append(c)
        return tuple(ret)

    def get_datatype(self, parent, data, key, model, schema) -> Union[DataType, None]:
        datatype_class = self.get_datatype_class(data.get("type", None))
        if datatype_class:
            return datatype_class(parent, data, key, model, schema)
        return None

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
        except:
            pass
        try:
            del self.components
        except:
            pass


datatypes = DataTypes()
