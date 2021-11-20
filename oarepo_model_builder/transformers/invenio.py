from oarepo_model_builder.schema import deepmerge
from oarepo_model_builder.transformers import ModelTransformer


class InvenioTransformer(ModelTransformer):

    def transform(self, schema, settings):
        deepmerge(settings, {
            'invenio': {
                'record_class': 'Record'
            }
        })
