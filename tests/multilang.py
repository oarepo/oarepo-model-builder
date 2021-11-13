from oarepo_model_builder.preprocessors import OutputPreprocessor, process
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.builders import ReplaceElement


class MultilangPreprocessor(OutputPreprocessor):
    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'multilingual')
    def modify_multilang_schema(self, data, stack, **kwargs):
        data['type'] = 'object'
        data['properties'] = {
            'lang': {
                'type': 'string'
            },
            'value': {
                'type': 'string'
            }
        }
        return data

    @process(model_builder=MappingBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'multilingual')
    def modify_multilang_mapping(self, data, stack, **kwargs):
        raise ReplaceElement({
            stack.top.key: {
                'type': 'object',
                'properties': {
                    'lang': {
                        'type': 'keyword'
                    },
                    'value': {
                        'type': 'text'
                    }
                }
            },
            stack.top.key + '_cs': {
                'type': 'text'
            }
        })
