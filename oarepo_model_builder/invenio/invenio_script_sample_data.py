import copy
from pathlib import Path

from oarepo_model_builder.stack import ModelBuilderStack
from ..builder import ModelBuilder
from ..builders import process
from ..builders.json_base import JSONBaseBuilder
from ..utils.schema import is_schema_element, match_schema, Ref

import faker


class InvenioScriptSampleDataBuilder(JSONBaseBuilder):
    TYPE = 'script_sample_data'
    output_file_type = 'yaml'
    output_file_name = 'script-import-sample-data'
    parent_module_root_name = 'jsonschemas'

    def __init__(self, builder: ModelBuilder):
        super().__init__(builder)
        self.faker = faker.Faker()

    def prepare(self, schema):
        output_name = self.settings[self.output_file_name]
        output = self.builder.get_output(self.output_file_type, output_name)
        if not output.created:
            return []
        count = schema.settings.get('oarepo:sample', {}).get('count', 50)
        return [copy.deepcopy(schema) for _ in range(count)]

    @process('/model/**', condition=lambda current, stack: is_schema_element(stack))
    def model_element(self, stack: ModelBuilderStack):
        schema_path = match_schema(stack)
        if isinstance(schema_path[-1], Ref):
            schema_element_type = schema_path[-1].element_type
        else:
            schema_element_type = None
        if schema_element_type == 'property':
            if not self.skip(stack):
                if 'properties' in stack.top.data:
                    self.output.enter(stack.top.key, {})
                elif 'items' in stack.top.data:
                    self.output.enter(stack.top.key, [])
                else:
                    self.output.primitive(stack.top.key, self.generate_fake(stack))
        yield
        if schema_element_type == 'property':
            if not self.skip(stack):
                if 'properties' in stack.top.data or 'items' in stack.top.data:
                    self.output.leave()

    def skip(self, stack):
        return stack.top.data.get('oarepo:sample', {}).get('skip', False)

    def on_enter_model(self, output_name, stack: ModelBuilderStack):
        self.output.next_document()

    def generate_fake(self, stack):
        params = {}
        method = None
        if 'oarepo:sample' in stack.top.data:
            config = stack.top.data['oarepo:sample']
            method = config.get('faker')
            params = config.get('params', params)

        if not method:
            if hasattr(self.faker, stack.top.key):
                method = stack.top.key
            else:
                method = 'sentence'
        return getattr(self.faker, method)()
