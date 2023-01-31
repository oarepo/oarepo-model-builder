from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.deepmerge import deepmerge


class OpensearchModelPreprocessor(ModelPreprocessor):
    TYPE = "opensearch"

    def transform(self, schema, settings):
        deepmerge(
            settings,
            {"opensearch": {"version": "os-v2"}},
        )
