import functools
import inspect
from collections import namedtuple

import oarepo_model_builder
from oarepo_model_builder.utils.json_pathlib import JSONPaths
from oarepo_model_builder.utils.stack import ModelBuilderStack


def _on(path, phase, priority, condition):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        wrapped.model_builder_phase = phase
        wrapped.model_builder_path = path
        wrapped.model_builder_priority = priority
        wrapped.model_builder_condition = condition
        return wrapped

    return wrapper


def on_enter(path, priority=0, condition=None):
    return _on(path, 'enter', priority, condition)


def on_leave(path, priority=0, condition=None):
    return _on(path, 'leave', priority, condition)


def on_primitive(path, priority=0, condition=None):
    return _on(path, 'primitive', priority, condition)


class OutputBuilder:
    output_builder_type = None
    PathMethodRecord = namedtuple('PathMethodRecord', 'phase, method')

    def __init__(self, builder: "oarepo_model_builder.builder.ModelBuilder"):
        self.builder = builder
        # TODO: move this to metaclass and initialize only once per class
        self.json_paths = JSONPaths()
        arr = []
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if not hasattr(method, 'model_builder_phase'):
                continue
            arr.append(
                (
                    -method.model_builder_priority,
                    -len(method.model_builder_path),
                    method.model_builder_path,
                    method.model_builder_phase,
                    id(method),
                    method.model_builder_condition,
                    method
                )
            )
        arr.sort()
        for _prior, _lpath, path, phase, _mid, condition, method in arr:
            self.json_paths.register(path, condition, OutputBuilder.PathMethodRecord(phase, method))

    def begin(self):
        pass

    def finish(self):
        pass

    def _call_method(self, stack: ModelBuilderStack, phase: str):
        for _phase, method in self.json_paths.match(stack.path, stack.top.el):
            if phase == _phase:
                return method(stack)

    def element_enter(self, stack: ModelBuilderStack):
        return self._call_method(stack, 'enter')

    def element_leave(self, stack: ModelBuilderStack):
        return self._call_method(stack, 'leave')

    def element_primitive(self, stack: ModelBuilderStack):
        return self._call_method(stack, 'primitive')


class OutputPreprocessor:
    PathMethodRecord = namedtuple('PathMethodRecord', 'phase, method, output_builder_type')

    def __init__(self, builder: "oarepo_model_builder.builder.ModelBuilder"):
        self.builder = builder
        # TODO: move this to metaclass and initialize only once per class
        self.json_paths = JSONPaths()
        arr = []
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if not hasattr(method, 'model_builder_phase'):
                continue
            arr.append(
                (
                    -method.model_builder_priority,
                    -len(method.model_builder_path),
                    method.model_builder_path,
                    method.model_builder_phase,
                    id(method),
                    method.model_builder_condition,
                    method.model_builder_output_builder_type,
                    method
                )
            )
        arr.sort()
        for _prior, _lpath, path, phase, _mid, condition, output_builder_type, method in arr:
            self.json_paths.register(path, condition,
                                     OutputPreprocessor.PathMethodRecord(phase, method, output_builder_type))

    def begin(self):
        pass

    def finish(self):
        pass

    def _call_method(self, data, stack: ModelBuilderStack, output_builder_type, phase: str):
        for _phase, method, _output_builder_type in self.json_paths.match(stack.path, stack.top.el):
            if phase == _phase and output_builder_type == _output_builder_type:
                return method(data, stack=stack)

    def enter(self, output_builder_type: str, data, stack: ModelBuilderStack):
        return self._call_method(data, stack, output_builder_type, 'enter')

    def primitive(self, output_builder_type: str, data, stack: ModelBuilderStack):
        return self._call_method(data, stack, output_builder_type, 'primitive')


def process(model_builder, phase, path, priority=0, condition=None):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        wrapped.model_builder_priority = priority
        wrapped.model_builder_phase = phase
        wrapped.model_builder_output_builder_type = model_builder if isinstance(model_builder, str) else model_builder.output_builder_type
        wrapped.model_builder_path = path
        wrapped.model_builder_condition = condition
        return wrapped

    return wrapper


class ReplaceElement:
    def __init__(self, data):
        self.data = data
