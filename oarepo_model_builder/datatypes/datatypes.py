from collections import namedtuple
from typing import List
import importlib_metadata
import copy

Import = namedtuple("Import", "import_path,alias")


class DataType:
    model_type = None
    marshmallow_field = None
    schema_type = None
    mapping_type = None
    use_dumper = False

    def __init__(self, definition):
        self.definition = definition

    def _copy_definition(self, **extras):
        ret = copy.deepcopy(self.definition)
        for k, v in extras.items():
            if k not in ret:
                ret[k] = v
        return ret

    def model_schema(self, **extras):
        return self._copy_definition(**extras)

    def json_schema(self, **extras):
        return self._copy_definition(type=self.schema_type, **extras)

    def mapping(self, **extras):
        return self._copy_definition(type=self.mapping_type, **extras)

    def marshmallow(self, **extras):
        ret = copy.deepcopy(self.definition.get("oarepo:marshmallow", {}))
        if self.marshmallow_field:
            ret.setdefault("field-class", self.marshmallow_field)
        ret.setdefault("validators", []).extend(self.marshmallow_validators)
        for k, v in extras.items():
            if k not in ret:
                ret[k] = v
        return ret

    def marshmallow_validators(self) -> List[str]:
        return []

    def imports(self, *extra) -> List[Import]:
        return extra

    def dump_to_search(self, data):
        return data

    def load_from_search(self, data):
        return data


class DataTypes:
    def __init__(self) -> None:
        self.datatypes = {}
        for entry in importlib_metadata.entry_points(
            group="oarepo_model_builder.datatypes"
        ):
            for dt in entry.load():
                self.datatypes[dt().model_type] = dt

    def get_datatype(self, data) -> DataType:
        ret = self.datatypes.get(data["type"])
        if ret:
            return ret(data)
        return None


datatypes = DataTypes()
