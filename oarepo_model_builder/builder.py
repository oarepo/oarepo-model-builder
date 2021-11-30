import copy
import importlib
from pathlib import Path
from typing import List, Dict, Type

from .builders import OutputBuilder, ModelBuilderStack, ReplaceElement
from .outputs import OutputBase
from .property_preprocessors import PropertyPreprocessor
from .schema import ModelSchema
from .model_preprocessors import ModelPreprocessor


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

    outputs: Dict[Path, OutputBase]
    """
    Mapping between concrete output (file path relative to output dir) and instance of builder class
    """

    property_preprocessors: List[PropertyPreprocessor]
    """
    Current instances of processor classes.
    """

    def __init__(
            self,
            outputs: List[type(OutputBase)] = (),
            output_builders: List[type(OutputBuilder)] = (),
            property_preprocessors: List[type(PropertyPreprocessor)] = (),
            model_preprocessors: List[type(ModelPreprocessor)] = (),
            open=open
    ):
        """
        Initializes the builder

        :param output_builders:          A list of extension classes to use in builds
        :param outputs:     List of file builder classes that generate files
        :param property_preprocessors: List of output type processor classes
        """
        self.output_builder_classes = [*output_builders]
        for o in outputs:
            assert o.TYPE, f'output_type not set up on class {o}'
        self.output_classes = [*outputs]
        self.property_preprocessor_classes = [*property_preprocessors]
        self.model_preprocessor_classes = [*model_preprocessors]
        self.filtered_output_classes = {o.TYPE: o for o in self.output_classes}
        self.open = open

    def get_output(self, output_type: str, path: str | Path):
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
    def build(self, schema: ModelSchema, output_dir: str | Path):
        """
        compile the schema to output directory

        :param schema:      the model schema
        :param output_dir:  output directory where to put generated files
        :return:            the outputs (self.outputs)
        """
        self.set_schema(schema)
        self.filtered_output_classes = {o.TYPE: o for o in self._filter_classes(self.output_classes, 'output')}
        self.output_dir = Path(output_dir).absolute()  # noqa
        self.outputs = {}
        self.output_builders = [e(self) for e in self._filter_classes(self.output_builder_classes, 'builder')]
        self.property_preprocessors = [e(self) for e in
                                       self._filter_classes(self.property_preprocessor_classes, 'property')]

        for model_preprocessor in self._filter_classes(self.model_preprocessor_classes, 'model'):
            model_preprocessor(self).transform(schema, schema.settings)

        # process the file
        self._iterate_schema(schema)

        for output in sorted(self.outputs.values(), key=lambda x: x.path):
            output.finish()

        return self.outputs

    def set_schema(self, schema):
        self.schema = schema
        self.settings = schema.settings

    # private methods

    def _filter_classes(self, classes: List[Type[object]], plugin_type):
        plugin_config = self.settings.plugins.get(plugin_type, None)
        if not plugin_config:
            return classes
        disabled = plugin_config.get('disabled', [])
        enabled = plugin_config.get('enabled', [])

        if disabled == '__all__':
            ret = []
        elif isinstance(disabled, (list, tuple)):
            ret = [c for c in classes if c.TYPE not in disabled]
        else:
            raise AttributeError('Value of settings.plugin.*.disabled must be either '
                                 'a list of names or string __all__ to disable all plugins.')
        if enabled:
            ret.extend(
                [c for c in classes if c.TYPE in enabled]
            )
            # add directly imported classes
            for en in enabled:
                if ':' in en:
                    en = en.split(':', maxsplit=1)
                    ret.append(getattr(importlib.import_module(en[0]), en[1]))
        return ret

    def _iterate_schema(self, schema: ModelSchema):
        for output_builder in self.output_builders:
            output_builder.begin(schema, schema.settings)

            for proc in self.property_preprocessors:
                proc.begin(schema, schema.settings)

            self._iterate_schema_output_builder(schema, output_builder)

            for proc in self.property_preprocessors:
                proc.finish()

            output_builder.finish()

    def _iterate_schema_output_builder(self, schema: ModelSchema, output_builder: OutputBuilder):
        def call_processors(stack, output_builder):
            data = copy.deepcopy(stack.top.data)
            for property_preprocessor in self.property_preprocessors:
                data = property_preprocessor.process(output_builder.TYPE, data, stack) or data
            return data

        def on_element(stack):
            data = call_processors(stack, output_builder)
            if isinstance(data, ReplaceElement):
                return data
            stack.top.data = data
            return output_builder.process_element(stack)

        ModelBuilderStack(schema).process(on_element)
