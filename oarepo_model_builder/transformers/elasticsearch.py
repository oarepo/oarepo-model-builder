from oarepo_model_builder.schema import deepmerge
from oarepo_model_builder.transformers import ModelTransformer


class ElasticsearchTransformer(ModelTransformer):

    def transform(self, schema, settings):
        deepmerge(
            settings,
            {
                'elasticsearch': {
                    'keyword_ignore_above': 50
                }
            }
        )
