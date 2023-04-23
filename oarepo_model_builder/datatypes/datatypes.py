import copy
from collections import namedtuple
from typing import List, Union, Any, Dict, Type

import importlib_metadata
import marshmallow as ma
from marshmallow import fields

from ..utils.facet_helpers import facet_definition, facet_name
from ..utils.import_class import import_class

from functools import lru_cache, cached_property
from ..utils.properties import class_property
from ..validation.utils import PermissiveSchema, StrictSchema, ImportSchema

Import = namedtuple("Import", "import_path,alias")


class PropertyMarshmallowSchema(StrictSchema):
    read = fields.Boolean(required=False)
    write = fields.Boolean(required=False)
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    field_name = fields.String(data_key="field-name", required=False)
    field = fields.String(required=False)
    field_class = fields.String(data_key="field-class", required=False)
    arguments = fields.List(fields.String(), required=False)
    validators = fields.List(fields.String(), required=False)


class PropertyUISchema(StrictSchema):
    marshmallow = fields.Nested(PropertyMarshmallowSchema)


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
        pass

    def __getattr__(self, name):
        """
        datatype.json_schema maps to self.definition['json-schema'].
        If it has not been found, an empty section is returned.

        At first _process_json_schema is called on the datatype, if it exists.

        Before returning, process_json_schema method is called on all components
        with datatype and section keyword arguments
        """
        if name.startswith("_process_"):
            return object.__getattr__(self, name)

        # get the section
        section_key = name.replace("_", "-")
        if section_key in self._sections:
            return self._sections[section_key]
        section = self.definition.get(section_key, {})
        section = copy.deepcopy(section)

        # call _process_ on self
        process_method = f"_process_{name}"
        if hasattr(self, process_method):
            getattr(self, process_method)(section=section)

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
    schema_type = None

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

        # marshmallow
        marshmallow = ma.fields.Nested(
            PropertyMarshmallowSchema,
            required=False,
        )

        # ui
        ui = ma.fields.Nested(
            PropertyUISchema,
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

        return type(
            f"{clz.__name__}ModelValidator",
            (*validators, clz.ModelSchema),
            {"Meta": Meta},
        )

    def _process_json_schema(self, section, **kwargs):
        section.setdefault("type", self.schema_type or self.definition["type"])

    def _process_mapping(self, section, **kwargs):
        stack = self.stack
        searchable = stack[0].definition.get("searchable", True)

        for p in reversed(stack[1:]):
            facets = p.facets
            if "searchable" in facets:
                searchable = facets["searchable"]
                break

        section.setdefault("type", self.mapping_type or self.definition["type"])
        if not searchable:
            section.setdefault("enabled", False)


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
        for c in datatype_components:
            # if c is a subclass of any other component, do not return it as it is overridden
            for cc in datatype_components:
                if cc != c and isinstance(cc, type(c)):
                    break
            else:
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
