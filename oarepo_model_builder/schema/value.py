import dataclasses
from enum import Enum
from pathlib import Path
from textwrap import indent
from typing import Any, Optional, Union


class ReferenceType(Enum):
    NONE = "none"
    REF = "ref"
    USE = "use"
    EXTEND = "extend"


@dataclasses.dataclass(frozen=True)
class SourcePart:
    reference_type: ReferenceType
    path: Optional[Path] = None
    include: Optional[str] = None
    content: Optional[Any] = None

    def __eq__(self, other):
        if not isinstance(other, SourcePart):
            return False
        return (
            self.reference_type == other.reference_type
            and self.path == other.path
            and self.include == other.include
        )

    def __hash__(self):
        return hash((self.reference_type, self.path, self.include))

    def __str__(self):
        return f"{self.reference_type.name} {self.path or self.include}"

    def __repr__(self):
        return str(self)


class Source(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)

    @property
    def previous(self):
        return Source(*self[:-1])

    @property
    def path(self):
        return self[-1].path

    @property
    def include(self):
        return self[-1].include

    @property
    def reference_type(self):
        return self[-1].reference_type

    @property
    def content(self):
        return self[-1].content

    @property
    def is_extended(self):
        return bool(any(part.reference_type == ReferenceType.EXTEND for part in self))

    def append(self, reference_type, path=None, include=None, content=None):
        if not self:
            return self.create(
                reference_type=reference_type,
                path=path,
                include=include,
                content=content,
            )
        if include:
            return Source(
                *self, SourcePart(reference_type, include=include, content=content)
            )

        parent = self.path
        return Source(
            *self, SourcePart(reference_type, path=parent / path, content=content)
        )

    @classmethod
    def create(cls, path=None, reference_type=ReferenceType.NONE, content=None):
        path = Path(path).resolve()
        if content is None:
            assert path.exists()
        return Source(SourcePart(reference_type, path=path, content=content))


@dataclasses.dataclass(frozen=True)
class Reference:
    source: Source
    fragment: str

    def extract_fragment(self, data):
        if self.fragment:
            if "/" in self.fragment:
                data = data.resolve_pointer(self.fragment)
            else:
                data = data.resolve_id(self.fragment)
        return data


class SchemaValue:
    def __init__(self, value, source, parent):
        self._parent = parent
        self._value = value
        assert isinstance(source, Source)
        self._source = source

    @property
    def value(self):
        return self._value

    def dump(self):
        if isinstance(self._value, dict):
            return {
                plain_key(k): v.dump() for k, v in self._value.items() if k != "$id"
            }
        elif isinstance(self._value, list):
            return [v.dump() for v in self._value]
        return self._value

    @property
    def parent(self):
        return self._parent

    @property
    def ancestors(self):
        ret = []
        p = self._parent
        while p:
            ret.append(p)
            p = p._parent
        return ret

    @property
    def source(self):
        return self._source

    @property
    def is_dict(self):
        return isinstance(self._value, dict)

    @property
    def is_list(self):
        return isinstance(self._value, list)

    @property
    def root(self):
        d = self
        while d._parent:
            d = d._parent
        return d

    def __contains__(self, item):
        return item in self._value

    def __getitem__(self, item):
        return self._value[item]

    def setdefault(self, key, value):
        if key in self:
            return self[key]
        self._value[key] = SchemaValue(value, self._source, self)
        return self._value[key]

    def __setitem__(self, key, value):
        if not self.is_dict:
            raise ValueError(f"Can not set item {key} in {self} - not a dict")
        if isinstance(value, SchemaValue):
            self._value[key] = value
            value._parent = self
        else:
            self._value[key] = SchemaValue.from_json(value, self._source, self)

    def values(self):
        if not self.is_dict:
            raise ValueError(f"Can not get values from {self} - not a dict")
        return self._value.values()

    def pop(self, key, default=None):
        return self._value.pop(key, default)

    def append(self, value):
        if not self.is_list:
            raise ValueError(f"Can not append to {self} - not a list")

        if isinstance(value, SchemaValue):
            self._value.append(value)
            value._parent = self
        else:
            self._value.append(SchemaValue.from_json(value, self._source, self))

    def merge_in(self, other, reference=None, **opts):
        if isinstance(self._value, dict):
            self._merge_dict(other, reference, **opts)
        elif isinstance(self._value, list):
            self._merge_list(other, reference, **opts)

    def _merge_dict(self, other, reference, **opts):
        if not other.is_dict:
            raise ValueError(f"Can not merge {other} into {self} - types do not match")

        plain_to_key = {}
        for k in self.value:
            pk = plain_key(k)
            if pk in plain_to_key:
                raise ValueError(f"Duplicate key {k} in {self}: {plain_to_key[pk]}")
            plain_to_key[pk] = k

        for other_key, other_value in sorted(other.value.items()):
            if other_key.startswith("*"):
                continue

            plain_other_key = plain_key(other_key)
            if f"!{plain_other_key}" in self.value:
                # my value overrides the one from the imported
                # TODO: store the imported value somewhere
                continue

            if plain_other_key not in plain_to_key:
                self._value[other_key] = other_value.duplicate()
                self._value[other_key]._parent = self
                continue

            my_key = plain_to_key[plain_other_key]

            # got at least one key, so need to merge those
            self._value[my_key].merge_in(
                other_value,
                reference,
                my_options=key_options(my_key),
                other_options=key_options(other_key),
            )

    def _merge_list(self, other, reference, my_options={}, other_options={}):
        if not other.value:
            return

        if not isinstance(other.value, list):
            raise ValueError(f"Can not merge {other} into {self} - types do not match")

        duplicated = [v.duplicate() for v in other.value]
        for v in duplicated:
            v._parent = self

        if my_options.get("append"):
            self._value = duplicated + self._value
        elif my_options.get("prepend"):
            self._value = self._value + duplicated
        elif other_options.get("prepend"):
            self._value = duplicated + self._value
        else:
            self._value = self._value + duplicated

    def duplicate(self):
        if isinstance(self._value, dict):
            return SchemaValue(
                {k: v.duplicate() for k, v in self._value.items()},
                self._source,
                self._parent,
            )
        if isinstance(self._value, list):
            return SchemaValue(
                [v.duplicate() for v in self._value],
                self._source,
                self._parent,
            )
        return SchemaValue(
            self._value,
            self._source,
            self._parent,
        )

    def resolve_pointer(self, pointer: Union[str, list[str]]):
        if not pointer:
            return self
        if isinstance(pointer, str):
            pointer = pointer.split("/")
        pointer = [x for x in pointer if x]
        if not isinstance(self._value, dict):
            raise ValueError(
                f"Can not resolve pointer {pointer} in {self} - types do not match"
            )
        return self._value[pointer[0]].resolve_pointer(pointer[1:])

    def resolve_id(self, _id: str):
        if not _id:
            return self
        if isinstance(self._value, dict):
            if "$id" in self._value and self._value["$id"].value == _id:
                return self
            for v in self._value.values():
                r = v.resolve_id(_id)
                if r:
                    return r
        elif isinstance(self._value, list):
            for v in self._value:
                r = v.resolve_id(_id)
                if r:
                    return r
        return None

    def __str__(self):
        return repr(self)

    def __repr__(self):
        src = ", ".join(str(x) for x in self._source)
        if isinstance(self._value, dict):
            ret = [f"{k}: {v}" for k, v in self._value.items()]
            ret = indent("\n".join(ret), "  ")
            return f"[{src}]\n{ret}"
        elif isinstance(self._value, list):
            ret = [f"{v}" for v in self._value]
            ret = indent("\n".join(ret), "  ")
            return f"[{src}]\n{ret}"
        return f"[{src}] {repr(self._value)}"

    @classmethod
    def from_json(cls, data, source: Source, parent: Optional["SchemaValue"]):
        if isinstance(data, dict):
            sv = SchemaValue({}, source, parent)
            for k, v in data.items():
                sv.value[k] = SchemaValue.from_json(v, source, sv)
            return sv
        if isinstance(data, list):
            sv = SchemaValue([], source, parent)
            for v in data:
                sv.value.append(SchemaValue.from_json(v, source, sv))
            return sv
        return SchemaValue(data, source, parent)


def plain_key(k):
    if k.startswith("!") or k.startswith(">") or k.startswith("<"):
        return plain_key(k[1:])
    return k


def key_options(k):
    if k.startswith("!"):
        return {"merge": False}
    if k.startswith(">"):
        return {"append": True}
    if k.startswith("<"):
        return {"prepend": True}
    return {}
