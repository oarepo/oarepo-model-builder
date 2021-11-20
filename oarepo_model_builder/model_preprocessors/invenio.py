from oarepo_model_builder.schema import deepmerge
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class InvenioModelPreprocessor(ModelPreprocessor):

    def transform(self, schema, settings):
        deepmerge(settings, {
            'invenio': {
                'record_class': 'Record'
            }
        })
