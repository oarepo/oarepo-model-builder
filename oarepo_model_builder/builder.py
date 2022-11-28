import copy
import importlib
import json
from pathlib import Path
from typing import Dict, List, Type, Union

import yaml

from .builders import (
    ModelBuilderStack,
    OutputBuilder,
    OutputBuilderComponent,
    ReplaceElement,
)
from .fs import AbstractFileSystem, FileSystem
from .model_preprocessors import ModelPreprocessor
from .outputs import OutputBase
from .property_preprocessors import PropertyPreprocessor
from .schema import ModelSchema
from .utils.cst import ConflictResolver
from .validation import validate_model


class ModelBuilder:
    """
    Processes a model file and generates/updates sources for the model
    """

    model_preprocessor_classes: List[type(ModelPreprocessor)]
    """
    Model preprocessor classes that are called after schema is loaded and before it is processed
    """

    output_classes: List[type(OutputBase)]
    """
    Mapping between output type and its handler class
    """

    filtered_output_classes: Dict[str, type(OutputBase)]
    """
    Filtered output classes by settings.plugins.disabled|enabled
    """

    output_builder_classes: List[type(OutputBuilder)]
    """
    A list of extension classes to be used in build. 
    """

    property_preprocessor_classes: List[type(PropertyPreprocessor)]
    """
    Processor classes (called before and after file builder is called)
    """

    output_builders: List[OutputBuilder]
    """
    A list of output_builders. Each extension is responsible for generating one or more files
    """

    output_builder_components: Dict[str, List[OutputBuilderComponent]]
    """
    A list of output builder components for an output builder
    """

    outputs: Dict[Path, OutputBase]
    """
    Mapping between concrete output (file path relative to output dir) and instance of builder class
    """

    property_preprocessors: List[PropertyPreprocessor]
    """
    Current instances of processor classes.
    """

    filesystem: AbstractFileSystem

    def __init__(
        self,
        outputs: List[type(OutputBase)] = (),
        output_builders: List[type(OutputBuilder)] = (),
        property_preprocessors: List[type(PropertyPreprocessor)] = (),
        model_preprocessors: List[type(ModelPreprocessor)] = (),
        output_builder_components: Dict[str, List[type(OutputBuilderComponent)]] = None,
        included_validation_schemas=None,
        filesystem=FileSystem(),
    ):
        """
        Initializes the builder

        :param output_builders:          A list of extension classes to use in builds
        :param outputs:     List of file builder classes that generate files
        :param property_preprocessors: List of output type processor classes
        """
        self.output_builder_classes = [*output_builders]
        for o in outputs:
            assert o.TYPE, f"output_type not set up on class {o}"
        self.output_classes = [*(outputs or [])]
        self.outputs = {}
        self.property_preprocessor_classes = [*(property_preprocessors or [])]
        self.model_preprocessor_classes = [*(model_preprocessors or [])]
        self.filtered_output_classes = {o.TYPE: o for o in self.output_classes}
        if output_builder_components:
            self.output_builder_components = {
                builder_type: [x() for x in components]
                for builder_type, components in output_builder_components.items()
            }
        else:
            self.output_builder_components = {}
        self.filesystem = filesystem
        self.included_validation_schemas = included_validation_schemas or []
        self.skip_schema_validation = False  # set to True in some tests

    def get_output(self, output_type: str, path: Union[str, Path]):
        """
        Given a path, instantiate file builder on the path with the given output type
        and return it. If the builder on the path has already been requested, return
        the same instance of the builder.

        :param output_type: @see FileBuilder.output_type
        :param path: relative path to output_dir, set in build()
        :return:    instance of FileBuilder for the path
        """
        if not isinstance(path, Path):
            path = Path(path)
        path = self.output_dir.joinpath(path)

        output = self.outputs.get(path, None)
        if output:
            assert output_type == self.outputs[path].TYPE
        else:
            output = self.filtered_output_classes[output_type](self, path)
            output.begin()
            self.outputs[path] = output
        return output

    def get_output_builder_components(self, output_builder_type):
        return self.output_builder_components.get(output_builder_type, ())

    # main entry point
    def build(
        self,
        model: ModelSchema,
        output_dir: Union[str, Path],
        resolver: ConflictResolver = None,
        overwrite = False
    ):
        """
        compile the schema to output directory

        :param model:      the model schema
        :param output_dir:  output directory where to put generated files
        :return:            the outputs (self.outputs)
        """
        if overwrite:
            if not hasattr(self.filesystem, 'overwrite'):
                raise AttributeError(
                    f'Filesystem of type {type(self.filesystem)} does not support overwrite')
            self.filesystem.overwrite = True

        self.conflict_resolver = resolver
        self.set_schema(model)
        self.filtered_output_classes = {
            o.TYPE: o for o in self._filter_classes(self.output_classes, "output")
        }
        self.output_dir = Path(output_dir).absolute()  # noqa
        self.outputs = {}
        self.overwrite = overwrite

        if not self.skip_schema_validation:
            validate_model(model, self.included_validation_schemas)

        for model_preprocessor in self._filter_classes(
            self.model_preprocessor_classes, "model"
        ):
            model_preprocessor(self).transform(model, model.settings)

        if not self.skip_schema_validation:
            validate_model(model, self.included_validation_schemas)

        # noinspection PyTypeChecker
        property_preprocessors: List[PropertyPreprocessor] = [
            e(self)
            for e in self._filter_classes(
                self.property_preprocessor_classes, "property"
            )
        ]

        output_builder_class: Type[OutputBuilder]
        for output_builder_class in self._filter_classes(
            self.output_builder_classes, "builder"
        ):
            output_builder = output_builder_class(
                builder=self, property_preprocessors=property_preprocessors
            )
            output_builder.build(model)

        self._save_outputs()

        return self.outputs

    def _save_outputs(self):
        for output in sorted(self.outputs.values(), key=lambda x: x.path):
            output.finish()
            if output.executable:
                self.filesystem.make_executable(output.path)

    def set_schema(self, schema):
        self.schema = schema
        self.settings = schema.settings

    # private methods

    def _filter_classes(self, classes: List[Type[object]], plugin_type):
        if (
            "plugins" not in self.schema.schema
            or plugin_type not in self.schema.schema.plugins
        ):
            return classes
        plugin_config = self.schema.schema.plugins[plugin_type]

        disabled = plugin_config.get("disable", [])
        enabled = plugin_config.get("enable", [])
        included = plugin_config.get("include", [])

        if included:
            enabled = [*enabled]  # will be adding inclusions so make a copy
            classes = [*classes]
            for incl in included:
                package_name, class_name = incl.split(":")
                class_type = getattr(importlib.import_module(package_name), class_name)
                classes.append(class_type)
                if enabled and class_type.TYPE not in enabled:
                    enabled.append(class_type.TYPE)

        if disabled == "__all__":
            ret = []
        else:
            ret = [c for c in classes if c.TYPE not in disabled]

        if enabled:
            ret.extend([c for c in classes if c.TYPE in enabled])
        return ret
