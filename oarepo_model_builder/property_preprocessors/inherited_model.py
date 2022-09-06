from oarepo_model_builder.builders.inherited_model import InheritedModelBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement
from oarepo_model_builder.stack.stack import RemoveElement


class InheritedModelPreprocessor(PropertyPreprocessor):
    TYPE = "inherited_model_preprocessor"

    @process(
        model_builder=InheritedModelBuilder,
        path="/settings"
    )
    def remove_settings(self, data, stack: ModelBuilderStack, **kwargs):
        raise RemoveElement()

    @process(
        model_builder=InheritedModelBuilder,
        path="/output-directory"
    )
    def remove_output_directory(self, data, stack: ModelBuilderStack, **kwargs):
        raise RemoveElement()
