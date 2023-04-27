import copy
from pathlib import Path
from typing import Dict, List, Type, Union

from .builders import OutputBuilder
from .datatypes.datatypes import datatypes
from .fs import AbstractFileSystem, FileSystem
from .model_preprocessors import ModelPreprocessor
from .outputs import OutputBase
from .schema import ModelSchema
from .utils.import_class import import_class
from .validation import validate_model


class ModelBuilder:
    """
    Processes a model file and generates/updates sources for the model
    """

    model_preprocessor_classes: List[Type[ModelPreprocessor]]
    """
    Model preprocessor classes that are called after schema is loaded and before it is processed
    """

    output_classes: List[Type[OutputBase]]
    """
    Mapping between output type and its handler class
    """

    filtered_output_classes: Dict[str, Type[OutputBase]]
    """
    Filtered output classes by settings.plugins.disabled|enabled
    """

    output_builder_classes: List[Type[OutputBuilder]]
    """
    A list of extension classes to be used in build. 
    """

    output_builders: List[OutputBuilder]
    """
    A list of output_builders. Each extension is responsible for generating one or more files
    """

    outputs: Dict[Path, OutputBase]
    """
    Mapping between concrete output (file path relative to output dir) and instance of builder class
    """

    filesystem: AbstractFileSystem

    overwrite: bool
    """
    If true, overwrite already existing files. If false, perform merge
    """

    def __init__(
        self,
        outputs: List[Type[OutputBase]] = (),
        output_builders: List[Type[OutputBuilder]] = (),
        model_preprocessors: List[Type[ModelPreprocessor]] = (),
        filesystem=FileSystem(),
        overwrite=False,
    ):
        """
        Initializes the builder

        :param output_builders:          A list of extension classes to use in builds
        :param outputs:     List of file builder classes that generate files
        """
        self.output_builder_classes = [*output_builders]
        for o in outputs:
            assert o.TYPE, f"output_type not set up on class {o}"
        self.output_classes = [*(outputs or [])]
        self.outputs = {}
        self.model_preprocessor_classes = [*(model_preprocessors or [])]
        self.filtered_output_classes = {o.TYPE: o for o in self.output_classes}
        self.filesystem = filesystem
        self.skip_schema_validation = False  # set to True in some tests
        self.overwrite = overwrite

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

    # main entry point
    def build(
        self,
        model: ModelSchema,
        output_dir: Union[str, Path],
        disable_validation: bool = False,
    ):
        """
        compile the schema to output directory

        :param model:      the model schema
        :param output_dir:  output directory where to put generated files
        :return:            the outputs (self.outputs)
        """

        # deep copy so that the passed model will not be influenced by preprocessors etc.
        model = copy.deepcopy(model)
        if self.overwrite:
            if not hasattr(self.filesystem, "overwrite"):
                raise AttributeError(
                    f"Filesystem of type {type(self.filesystem)} does not support overwrite"
                )
            self.filesystem.overwrite = True

        self.set_schema(model)
        self.filtered_output_classes = {
            o.TYPE: o for o in self._filter_classes(self.output_classes, "output")
        }
        self.output_dir = Path(output_dir).absolute()  # noqa
        self.outputs = {}

        if not disable_validation:
            self._validate_model(model)

        self._run_model_preprocessors(model)

        if not disable_validation:
            self._validate_model(model)

        self._run_output_builders(model)

        self._save_outputs()

        return self.outputs

    def _run_output_builders(self, model):
        output_builder_class: Type[OutputBuilder]
        for output_builder_class in self._filter_classes(
            self.output_builder_classes, "builder"
        ):
            output_builder = output_builder_class(builder=self)
            current_model = datatypes.get_datatype(
                parent=None,
                data=model.current_model,
                key=None,
                model=model.current_model,
                schema=model.schema,
            )
            current_model.prepare({})
            output_builder.build(current_model=current_model, schema=model.schema)

    def _run_model_preprocessors(self, model):
        for model_preprocessor in self._filter_classes(
            self.model_preprocessor_classes, "model"
        ):
            model_preprocessor(self).transform(model, model.settings)

    def _validate_model(self, model):
        if not self.skip_schema_validation:
            validate_model(model)

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
            "plugins" not in self.schema.current_model
            or plugin_type not in self.schema.current_model["plugins"]
        ):
            return classes
        plugin_config = self.schema.current_model["plugins"][plugin_type]

        disabled = plugin_config.get("disable", [])
        enabled = plugin_config.get("enable", [])
        included = plugin_config.get("include", [])

        if included:
            enabled = [*enabled]  # will be adding inclusions so make a copy
            classes = [*classes]
            for incl in included:
                class_type = import_class(incl)
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
