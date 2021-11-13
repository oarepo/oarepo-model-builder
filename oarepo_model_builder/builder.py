import copy
import os
from typing import List, Dict

from .outputs import OutputBase
from .schema import ModelSchema
from .transformers import ModelTransformer
from .builders import OutputBuilder, ModelBuilderStack, ReplaceElement
from .preprocessors import OutputPreprocessor


class ModelBuilder:
    """
    Processes a model file and generates/updates sources for the model
    """

    transformer_classes: List[type(ModelTransformer)]
    """
    Transformer classes that are called after schema is loaded and before it is processed
    """

    output_classes: Dict[str, type(OutputBase)]
    """
    Mapping between output type and its handler class
    """

    output_builder_classes: List[type(OutputBuilder)]
    """
    A list of extension classes to be used in build. 
    """

    output_preprocessor_classes: List[type(OutputPreprocessor)]
    """
    Processor classes (called before and after file builder is called)
    """

    output_builders: List[OutputBuilder]
    """
    A list of output_builders. Each extension is responsible for generating one or more files
    """

    outputs: Dict[str, OutputBase]
    """
    Mapping between concrete output (file path relative to output dir) and instance of builder class
    """

    output_preprocessors: List[OutputPreprocessor]
    """
    Current instances of processor classes.
    """

    def __init__(
            self,
            outputs: List[type(OutputBase)] = (),
            output_builders: List[type(OutputBuilder)] = (),
            output_preprocessors: List[type(OutputPreprocessor)] = (),
            transformers: List[type(ModelTransformer)] = ()
    ):
        """
        Initializes the builder

        :param output_builders:          A list of extension classes to use in builds
        :param outputs:     List of file builder classes that generate files
        :param output_preprocessors: List of output type processor classes
        """
        self.output_builder_classes = [*output_builders]
        for o in outputs:
            assert o.output_type, f'output_type not set up on class {o}'
        self.output_classes = {o.output_type: o for o in outputs}
        self.output_preprocessor_classes = [*output_preprocessors]
        self.transformer_classes = [*transformers]

    def get_output(self, output_type: str, path: str):
        """
        Given a path, instantiate file builder on the path with the given output type
        and return it. If the builder on the path has already been requested, return
        the same instance of the builder.

        :param output_type: @see FileBuilder.output_type
        :param path: relative path to output_dir, set in build()
        :return:    instance of FileBuilder for the path
        """
        output = self.outputs.get(path, None)
        if output:
            assert output_type == self.outputs[path].output_type
        else:
            output = self.output_classes[output_type](os.path.join(self.output_dir, path))
            output.begin()
            self.outputs[path] = output
        return output

    # main entry point
    def build(self, schema: ModelSchema, output_dir):
        """
        compile the schema to output directory

        :param schema:      the model schema
        :param output_dir:  output directory where to put generated files
        :return:            the outputs (self.outputs)
        """
        self.output_dir = output_dir  # noqa
        self.outputs = {}
        self.output_builders = [e(self) for e in self.output_builder_classes]
        self.output_preprocessors = [e(self) for e in self.output_preprocessor_classes]

        for ext in self.output_builders:
            ext.begin()

        for proc in self.output_preprocessors:
            proc.begin()

        for transformer in self.transformer_classes:
            schema = transformer(self).transform(schema) or schema

        # process the file
        self._iterate_schema(schema)

        for proc in self.output_preprocessors:
            proc.finish()

        for ext in self.output_builders:
            ext.finish()

        for output in self.outputs.values():
            output.finish()

        return self.outputs

    # private methods

    def _iterate_schema(self, schema: ModelSchema):
        for output_builder in self.output_builders:
            self._iterate_schema_output_builder(schema, output_builder)

    def _iterate_schema_output_builder(self, schema: ModelSchema, output_builder: OutputBuilder):
        def call_processors(stack, output_builder):
            data = copy.deepcopy(stack.top.data)
            for output_preprocessor in self.output_preprocessors:
                data = output_preprocessor.process(output_builder.output_builder_type, data, stack) or data
            return data

        def on_element(stack):
            data = call_processors(stack, output_builder)
            if isinstance(data, ReplaceElement):
                return data
            stack.top.data = data
            return output_builder.process_element(stack)

        ModelBuilderStack(schema).process(on_element)
