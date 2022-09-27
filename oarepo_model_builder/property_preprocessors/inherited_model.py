from oarepo_model_builder.builders.inherited_model import InheritedModelBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement
from oarepo_model_builder.stack.stack import RemoveElement


class InheritedModelPreprocessor(PropertyPreprocessor):
    TYPE = "inherited_model_preprocessor"

    @process(model_builder=InheritedModelBuilder, path="/settings$")
    def replace_settings(self, data, stack: ModelBuilderStack, **kwargs):
        if "for-inheritance" in data:
            return data
        new_settings = self._replace_settings_for_inheritance(data)
        new_settings["for-inheritance"] = True
        raise ReplaceElement({"settings": new_settings})

    def _replace_settings_for_inheritance(self, settings):
        new_settings = {}
        for k, v in settings.items():
            if k.endswith("-class"):
                new_settings[k.replace("-class", "-base-classes")] = [v]
            if isinstance(v, dict):
                new_settings[k] = self._replace_settings_for_inheritance(v)
        return new_settings

    @process(model_builder=InheritedModelBuilder, path="/output-directory$")
    def remove_output_directory(self, data, stack: ModelBuilderStack, **kwargs):
        raise RemoveElement()
