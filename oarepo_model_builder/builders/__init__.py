from __future__ import annotations

import functools
import inspect
from typing import TYPE_CHECKING

from oarepo_model_builder.utils.json_pathlib import JSONPaths
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement
from oarepo_model_builder.utils.verbose import log

if TYPE_CHECKING:
    from oarepo_model_builder.builder import ModelBuilder


def process(path, priority=0, condition=None):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        wrapped.model_builder_path = path
        wrapped.model_builder_priority = priority
        wrapped.model_builder_condition = condition
        return wrapped

    return wrapper


class OutputBuilder:
    TYPE = None

    def __init__(self, builder: ModelBuilder):
        self.builder = builder
        # TODO: move this to metaclass and initialize only once per class
        self.json_paths = JSONPaths()
        arr = []
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if not hasattr(method, 'model_builder_priority'):
                continue
            arr.append(
                (
                    -method.model_builder_priority,
                    -len(method.model_builder_path),
                    method.model_builder_path,
                    id(method),
                    method.model_builder_condition,
                    method
                )
            )
        arr.sort()
        for _prior, _lpath, path, _mid, condition, method in arr:
            self.json_paths.register(path, condition, method)

    def begin(self, schema, settings):
        self.schema = schema
        self.settings = settings
        log.enter(2, 'Creating %s', self.TYPE)
        pass

    def finish(self):
        log.leave()

    def process_element(self, stack: ModelBuilderStack):
        """
        Normally returns a generator with a single yield:
        1. first part is called on element start
        2. yield causes that the content of the element is processed
        3. generator is called again to finish the element

        If no generator is returned, the content of the element is not processed
        """
        for method in self.json_paths.match(stack.path, stack.top.data, extra_data={
            'stack': stack
        }):
            return method(stack)
        # do not skip stack top
        if stack.level > 1:
            return stack.SKIP

    @process('/model')
    def enter_model(self, stack: ModelBuilderStack):
        # do not skip /model
        yield


__all__ = [
    'process',
    'OutputBuilder',
    'ModelBuilderStack',
    'ReplaceElement'
]
