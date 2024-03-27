from typing import List

from oarepo_model_builder.schema.value import (
    Reference,
    ReferenceType,
    SchemaValue,
    Source,
)


class SchemaLoader:
    USE_KEYWORD = "use"
    REF_KEYWORD = "$ref"
    EXTEND_KEYWORD = "extend"

    def __init__(
        self,
        loaders,
        schemas_by_name,
        reference_processors=None,
        post_reference_processors=None,
    ):
        self.loaders = loaders
        self.schemas_by_name = schemas_by_name
        self.reference_processors = reference_processors or {}
        self.post_reference_processors = post_reference_processors or {}
        self.cache = {}

    def load(self, source: Source, content=None):
        if not source.content and source in self.cache:
            data = self.cache[source]
        elif content:
            data = SchemaValue.from_json(content, source, None)
        else:
            data = self._load_data_from_file(source)
            if not source.content:
                self.cache[source] = data

        self._resolve(data)
        return data

    def _load_data_from_file(self, source: Source):
        if source.content is not None:
            return SchemaValue.from_json(source.content, source, None)
        path = source.path
        raw_value = self._load_raw_data_from_file(path)
        return SchemaValue.from_json(raw_value, source, None)

    def _load_raw_data_from_file(self, path):
        extension = path.suffix.lower()[1:]
        if extension not in self.loaders:
            raise RuntimeError(
                f"Can not load {path} - no loader has been found for extension {extension} "
                f"in entry point group oarepo_model_builder.loaders"
            )
        raw_value = self.loaders[extension](path)
        return raw_value

    def _resolve(self, data: SchemaValue):
        unresolved_values = [data]
        while unresolved_values:
            current = unresolved_values.pop()
            self._resolve_value(current, unresolved_values, data)

    def _resolve_value(self, value: SchemaValue, unresolved_values, root):
        if value.is_dict:
            references = self._get_references(value)
            for reference in references:
                if reference.source == value.source:
                    resolved = value.root
                else:
                    resolved = self._load_data_from_file(reference.source)
                resolved = reference.extract_fragment(resolved)
                value.merge_in(resolved)

            if references:
                # run again to resolve the references
                unresolved_values.append(value)
            else:
                # continue to children
                unresolved_values.extend(value.value.values())
        elif value.is_list:
            unresolved_values.extend(value.value)

    def _get_references(self, value) -> List[Reference]:
        ret = []
        if self.REF_KEYWORD in value.value:
            for ref in as_list(value.pop(self.REF_KEYWORD)):
                ret.append(self._resolve_by_name(ReferenceType.REF, ref))
            return ret
        if self.USE_KEYWORD in value.value:
            for ref in as_list(value.pop(self.USE_KEYWORD)):
                ret.append(self._resolve_by_name(ReferenceType.USE, ref))
            return ret
        if self.EXTEND_KEYWORD in value.value:
            for ref in as_list(value.pop(self.EXTEND_KEYWORD)):
                ret.append(self._resolve_by_name(ReferenceType.EXTEND, ref))
            return ret
        return []

    def _resolve_by_name(self, reference_type, ref: SchemaValue) -> Reference:
        path_or_name = ref.value
        if "#" in path_or_name:
            path_or_name, fragment = path_or_name.split("#", 1)
        else:
            fragment = None

        if path_or_name in self.schemas_by_name:
            included = self.schemas_by_name[path_or_name]
            if callable(included):
                return Reference(
                    ref.source.append(
                        reference_type, include=ref.value, content=included(self)
                    ),
                    fragment,
                )
            return Reference(ref.source.append(reference_type, path=included), fragment)
        if not path_or_name or path_or_name == ".":
            return Reference(ref.source, fragment)
        return Reference(ref.source.append(reference_type, path=ref.value), fragment)


def as_list(value) -> List[SchemaValue]:
    if not value:
        return []
    if isinstance(value, SchemaValue):
        if not isinstance(value.value, (list, tuple)):
            return [value]
        return value.value
    raise ValueError(f"Expected list or SchemaValue, got {value}")
