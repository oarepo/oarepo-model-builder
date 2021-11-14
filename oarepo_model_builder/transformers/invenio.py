from oarepo_model_builder.transformers import ModelTransformer


class InvenioTransformer(ModelTransformer):

    def transform(self, schema):
        invenio = schema.schema.setdefault('invenio', {})
        package = schema.schema.get('package')

        invenio.set_default('record_class', 'Record')
