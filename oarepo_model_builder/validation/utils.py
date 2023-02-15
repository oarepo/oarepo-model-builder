import re
import typing
from functools import cached_property

import marshmallow as ma
from marshmallow import fields
from marshmallow.error_store import ErrorStore
from marshmallow.exceptions import ValidationError


class CheckedConstant(fields.Constant):
    def _deserialize(self, value, *args, **kwargs):
        if value != self.constant:
            raise ValidationError(f"Bad value: '{self.constant}' expected.")
        return super()._deserialize(value, *args, **kwargs)


class ExtendablePartSchema(ma.Schema):
    extend = fields.String(required=False)
    use = fields.String(required=False)


class RegexOpts(ma.SchemaOpts):
    def __init__(self, meta, **kwargs):
        super().__init__(meta, **kwargs)
        self.regex_fields = getattr(meta, "regex_fields", [])


class RegexFieldsSchema(ma.Schema):
    OPTIONS_CLASS = RegexOpts

    def _deserialize(
        self,
        data: typing.Union[
            typing.Mapping[str, typing.Any],
            typing.Iterable[typing.Mapping[str, typing.Any]],
        ],
        *,
        error_store: ErrorStore,
        many: bool = False,
        partial=False,
        unknown=ma.RAISE,
        index=None,
    ):
        loaded = super()._deserialize(
            data,
            error_store=error_store,
            many=many,
            partial=partial,
            unknown=ma.EXCLUDE,  # exclude unknown - will be handled by the regex
            index=index,
        )
        # load all regex fields
        if many:
            for (loaded_data, orig_data) in zip(loaded, data):
                self.load_regex_fields(loaded_data, orig_data, error_store, index)
        else:
            self.load_regex_fields(loaded, data, error_store, index)
        return loaded

    @cached_property
    def compiled_regex_fields(self):
        return [(re.compile(x["key"]), x["field"]) for x in self.opts.regex_fields]

    def load_regex_fields(self, loaded_data, data, error_store, index):
        index_errors = self.opts.index_errors

        for fld in data:
            if fld in loaded_data:
                continue

            for fld_regex, field in self.compiled_regex_fields:
                if fld_regex.match(fld):
                    field = field()
                    self._bind_field(fld, field)
                    try:
                        loaded_data[fld] = field.deserialize(data[fld], fld, data)
                    except ValidationError as error:
                        error_store.store_error(error.messages, fld, index=index)
                    break

        data_keys = set(data.keys())
        loaded_keys = set(loaded_data.keys())
        for key in data_keys - loaded_keys:
            error_store.store_error(
                [self.error_messages["unknown"]],
                key,
                (index if index_errors else None),
            )

    def _serialize(self, obj, *, many: bool = False):
        serialized = super()._serialize(obj, many=many)
        if many:
            for (serialized_data, orig_data) in zip(serialized, obj):
                self.save_regex_fields(serialized_data, orig_data)
        else:
            self.save_regex_fields(serialized, obj)
        return serialized

    def save_regex_fields(self, serialized, obj):
        for attr_name in obj:
            if attr_name in serialized:
                continue

            for fld_regex, field in self.compiled_regex_fields:
                if fld_regex.match(attr_name):
                    self.save_regex_field(serialized, attr_name, field, obj)
                    break

    def save_regex_field(self, serialized, attr_name, field, obj):
        field = field()
        self._bind_field(attr_name, field)

        value = field.serialize(attr_name, obj, accessor=self.get_attribute)
        if value is ma.missing:
            return
        key = field.data_key if field.data_key is not None else attr_name
        serialized[key] = value


class PermissiveSchema(ExtendablePartSchema):
    class Meta:
        unknown = ma.INCLUDE

    def dump(self, obj, *, many=None):
        if not obj:
            return super().dump(obj, many=many)
        if many:
            return [self.dump(x, many=False) for x in obj]
        return {**obj, **super().dump(obj, many=False)}
