from collections import defaultdict

from oarepo_model_builder.builders import process
from oarepo_model_builder.stack import ModelBuilderStack
from .invenio_base import InvenioBaseClassPythonBuilder
from ..outputs.json_stack import JSONStack
from ..utils.schema import is_schema_element


class InvenioRecordSchemaBuilder(InvenioBaseClassPythonBuilder):
    class_config = 'record-schema-class'
    template = 'record-schema'

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.stack = JSONStack()
        self.imports = defaultdict(set)  # import => aliases

    def finish(self):
        # TODO: generate subschemas as well, not implemented here
        # TODO: generate arrays as well, not implemented here
        super().finish(fields=self.stack.value.get('properties', {}), imports=self.imports)

    @process('/model/**', condition=lambda current: is_schema_element(current.stack))
    def enter_model_element(self, stack: ModelBuilderStack):
        self.model_element_enter(stack)

        # process children
        yield

        data = stack.top.data
        if isinstance(data, dict):
            set_definition = False
            if 'oarepo:marshmallow' in data:
                self.stack.push('oarepo:marshmallow', data['oarepo:marshmallow'])
                self.stack.pop()
                set_definition = True
            elif stack.stack[-2].key == 'properties':
                self.stack.push(
                    'oarepo:marshmallow', {})

                self.stack.pop()
                set_definition = True
            if set_definition:
                self.set_marshmallow_definition(self.stack.real_top)

        self.model_element_leave(stack)

    def set_marshmallow_definition(self, data):
        marshmallow = data['oarepo:marshmallow']
        for imp in marshmallow.get('imports', []):
            self.imports[imp['import']].add(imp['prefix'])

        if 'field' in marshmallow:
            return
        data_type = data.get('type', 'object')
        generator = self.schema.settings.python.marshmallow.mapping.get(data_type, None)
        if not generator:
            generator = default_marshmallow_generators.get(data_type, None)
            if not generator:
                raise Exception(f'Do not have marshmallow field generator for {data_type}. '
                                f'Define it either in invenio_record_schema.py or in your own config')
        marshmallow['field'] = generator(data, self.schema, self.imports)

    def model_element_enter(self, stack: ModelBuilderStack):
        top = stack.top
        match stack.top_type:
            case stack.PRIMITIVE:
                self.stack.push(top.key, top.data)
            case stack.LIST:
                self.stack.push(top.key, [])
            case stack.DICT:
                self.stack.push(top.key, {})

    def model_element_leave(self, stack: ModelBuilderStack):
        self.stack.pop()


# TODO: how to do required ? Need to do this later, on leave of 'properties'
def marshmallow_string_generator(data, schema, imports):
    add_imports(imports)
    opts = []
    validators = []
    min_length = data.get('minLength', None)
    max_length = data.get('maxLength', None)
    if min_length is not None or max_length is not None:
        validators.append(f'ma_valid.Length(min={min_length}, max={max_length})')
    if validators:
        opts.append(f'validators=[{",".join(validators)}]')
    return f'ma.String({", ".join(opts)})'


def add_imports(imports):
    imports['marshmallow.fields'].add('ma')
    imports['marshmallow.validate'].add('ma_valid')


default_marshmallow_generators = {
    'string': marshmallow_string_generator
}
