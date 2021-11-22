from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class ElasticsearchModelPreprocessor(ModelPreprocessor):
    TYPE = 'elasticsearch'

    def transform(self, schema, settings):
        deepmerge(
            settings,
            {
                'elasticsearch': {
                    'keyword-ignore-above': 50
                }
            }
        )
