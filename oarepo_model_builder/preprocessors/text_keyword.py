from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.schema import deepmerge
from oarepo_model_builder.stack import ModelBuilderStack


class TextKeywordPreprocessor(PropertyPreprocessor):

    #
    # type='fulltext' in model
    #

    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'fulltext')
    def modify_fulltext_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'string'
        return data

    @process(model_builder=MappingBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'fulltext')
    def modify_fulltext_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'text'
        return data

    #
    # type='keyword' in model
    #

    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'keyword')
    def modify_keyword_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'string'
        return data

    @process(model_builder=MappingBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'keyword')
    def modify_keyword_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'keyword'
        data['ignore_above'] = self.settings['elasticsearch']['keyword_ignore_above']
        return data

    #
    # type='fulltext-keyword' in model
    #

    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'fulltext-keyword')
    def modify_fulltext_keyword_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'string'
        return data

    @process(model_builder=MappingBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'fulltext-keyword')
    def modify_fulltext_keyword_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'text'
        return deepmerge(data, {
            'fields': {
                'keyword': {
                    'type': 'keyword',
                    'ignore_above': self.settings['elasticsearch']['keyword_ignore_above']
                }
            }
        }, [])
