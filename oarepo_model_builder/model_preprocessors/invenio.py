from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


def last_item(x):
    return x.rsplit('.', maxsplit=1)[-1]


class InvenioModelPreprocessor(ModelPreprocessor):

    def transform(self, schema, settings):
        deepmerge(settings, {
            'python': {
                'record-class': settings.package + '.records.Record',
                'record-metadata-class': (settings.package + '.metadata.RecordMetadata'),
                'record-dumper-class': settings.package + '.dumpers.RecordDumper',
                # just make sure that the templates is always there
                'templates': {
                }
            }
        })

        self.set(settings.python, 'record-metadata-table-name',
                 lambda: f'{last_item(settings.package)}_{last_item(settings.python.record_metadata_class).lower()}')
