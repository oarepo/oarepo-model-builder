from __future__ import annotations

import functools
import inspect
from collections import namedtuple
from typing import TYPE_CHECKING

from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.json_pathlib import JSONPaths

if TYPE_CHECKING:
    from oarepo_model_builder.builder import ModelBuilder


class PropertyPreprocessor:
    PathMethodRecord = namedtuple("PathMethodRecord", "method, output_builder_type")

    def __init__(self, builder: ModelBuilder):
        self.builder = builder
        # TODO: move this to metaclass and initialize only once per class
        self.json_paths = JSONPaths()
        arr = []
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if not hasattr(method, "model_builder_priority"):
                continue
            for ot in method.model_builder_output_builder_types:
                arr.append(
                    (
                        -method.model_builder_priority,
                        -len(method.model_builder_path),
                        method.model_builder_path,
                        id(method),
                        method.model_builder_condition,
                        ot,
                        method,
                    )
                )
        arr.sort()
        for _prior, _lpath, path, _mid, condition, output_builder_type, method in arr:
            self.json_paths.register(
                path,
                condition,
                PropertyPreprocessor.PathMethodRecord(method, output_builder_type),
            )

    def begin(self, schema, settings):
        self.schema = schema
        self.settings = settings

    def finish(self):
        pass

    def _call_method(self, data, stack: ModelBuilderStack, output_builder_type):
        for method, _output_builder_type in self.json_paths.match(
            stack.path, stack.top.data, extra_data={"stack": stack}
        ):
            if (
                _output_builder_type == "*"
                or output_builder_type == _output_builder_type
            ):
                return method(
                    data, stack=stack, output_builder_type=output_builder_type
                )

    def process(self, output_builder_type: str, data, stack: ModelBuilderStack):
        return self._call_method(data, stack, output_builder_type)


def process(model_builder, path, priority=0, condition=None):
    """
    :param model_builder either a single builder, its TYPE property or a list of builders or their TYPEs
    :param path A single path or a tuple of paths that must be matched. May contain '**' which means 1+ path segments,
                * which means single path segment (for example properties/blah might is matched by **
                or properties/*)
    """

    def convert_type(model_builder_types):
        if not isinstance(model_builder_types, (list, tuple)):
            model_builder_types = [model_builder_types]
        return [
            model_builder if isinstance(model_builder, str) else model_builder.TYPE
            for model_builder in model_builder_types
        ]

    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        wrapped.model_builder_priority = priority
        wrapped.model_builder_output_builder_types = convert_type(model_builder)
        wrapped.model_builder_path = path
        wrapped.model_builder_condition = condition
        return wrapped

    return wrapper
