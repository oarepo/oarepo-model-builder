import copy
from collections import namedtuple
from typing import List, Union

import importlib_metadata
import marshmallow as ma
from marshmallow import fields

Import = namedtuple("Import", "import_path,alias")


class DataType:
    model_type = None
    marshmallow_field = None
    ui_marshmallow_field = None
    schema_type = None
    mapping_type = None

    class ModelSchema(ma.Schema):
        type = fields.String(required=True)

    def __init__(self, definition, key, model, schema, stack):
        self.definition = definition
        self.key = key
        self.model = model
        self.schema = schema
        self.stack = stack

    def _copy_definition(self, **extras):
        ret = copy.deepcopy(self.definition)
        for k, v in extras.items():
            if v is not None:
                ret[k] = v
        return ret

    def model_schema(self, **_extras):
        return None

    def json_schema(self, **extras):
        return self._copy_definition(type=self.schema_type, **extras)

    def mapping(self, **extras):
        return self._copy_definition(type=self.mapping_type, **extras)

    def marshmallow(self, **extras):
        ret = copy.deepcopy(self.definition.get("marshmallow", {}))
        if self.marshmallow_field:
            ret.setdefault("field-class", self.marshmallow_field)
        ret.setdefault("validators", []).extend(self.marshmallow_validators())
        for k, v in extras.items():
            if v is not None:
                ret[k] = v
        return ret

    def ui_marshmallow(self, **extras):
        ui = self.definition.get("ui", {})
        if "marshmallow" in ui:
            ret = copy.deepcopy(ui.get("marshmallow", {}))
        else:
            ret = copy.deepcopy(self.definition.get("marshmallow", {}))
        if self.ui_marshmallow_field:
            ret.setdefault("field-class", self.ui_marshmallow_field)
        elif self.marshmallow_field:
            ret.setdefault("field-class", self.marshmallow_field)
        # no validators for ui, as it is dump only
        for k, v in extras.items():
            if v is not None:
                ret[k] = v
        return ret

    def marshmallow_validators(self) -> List[str]:
        return []

    def imports(self, *extra) -> List[Import]:
        return extra

    def dumper_class(self, data):  # NOSONAR
        return None


class DataTypes:
    def __init__(self) -> None:
        self.datatype_map = {}

    def _prepare_datatypes(self):
        if not self.datatype_map:
            for entry in importlib_metadata.entry_points(
                group="oarepo_model_builder.datatypes"
            ):
                for dt in entry.load():
                    self.datatype_map[dt.model_type] = dt

    def get_datatype(self, data, key, model, schema, stack) -> Union[DataType, None]:
        datatype_class = self.get_datatype_class(data.get("type", None))
        if datatype_class:
            return datatype_class(data, key, model, schema, stack)
        return None

    def get_datatype_class(self, datatype_type):
        self._prepare_datatypes()
        return self.datatype_map.get(datatype_type)

    def facet(self, stack):
        facet, path = stack[0].get_facet(stack[1:], "")
        return facet, path


datatypes = DataTypes()
