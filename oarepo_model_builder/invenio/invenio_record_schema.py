from collections import defaultdict

from oarepo_model_builder.builders import process
from oarepo_model_builder.stack import ModelBuilderStack
from .invenio_base import InvenioBaseClassPythonBuilder
from ..outputs.json_stack import JSONStack
from ..utils.deepmerge import deepmerge
from ..utils.schema import is_schema_element


class InvenioRecordSchemaBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_record_schema'
    class_config = 'record-schema-class'
    template = 'record-schema'

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.stack = JSONStack()
        self.imports = defaultdict(set)  # import => aliases
        self.imports['marshmallow'].add('ma')
        self.imports['marshmallow.fields'].add('ma_fields')
        self.imports['marshmallow.validate'].add('ma_valid')

    def finish(self):
        # TODO: generate subschemas as well
        # TODO: generate arrays as well
        # TODO: handle required
        super().finish(
            fields=self.stack.value.get('properties', {}),
            imports=self.imports,

        )

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

        data_type = data.get('type', 'object')
        generator = self.schema.settings.python.marshmallow.mapping.get(data_type, None)
        if isinstance(generator, dict):
            # a value, not a callable => merge it
            marshmallow = deepmerge(generator, marshmallow)
            data['marshmallow'] = marshmallow
            generator = None

        # add imports if required
        for imp in marshmallow.get('imports', []):
            self.imports[imp['import']].add(imp['alias'])

        if 'field' in marshmallow:
            # do not modify the field
            return
        if 'class' in marshmallow:
            # generate instance of the class, filling the options and validators
            marshmallow['field'] = create_field(marshmallow['class'], options=(), validators=(), data=data)
            return

        # if no generator from settings, get the default one
        if not generator:
            generator = default_marshmallow_generators.get(data_type, None)
            if not generator:
                raise Exception(f'Do not have marshmallow field generator for {data_type}. '
                                f'Define it either in invenio_record_schema.py or in your own config')

        # and generate the field
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


def create_field(field_type, options=(), validators=(), data=None):
    opts = [*options, *data['oarepo:marshmallow'].get('options', [])]
    validators = [*validators, *data['oarepo:marshmallow'].get('validators', [])]
    nested = data['oarepo:marshmallow'].get('nested', False)
    if validators:
        opts.append(f'validate=[{",".join(validators)}]')
    ret = f'{field_type}({", ".join(opts)})'
    if nested:
        ret = f'ma_fields.Nested({ret})'
    return ret


def marshmallow_string_generator(data, schema, imports):
    validators = []
    min_length = data.get('minLength', None)
    max_length = data.get('maxLength', None)
    if min_length is not None or max_length is not None:
        validators.append(f'ma_valid.Length(min={min_length}, max={max_length})')
    return create_field('ma_fields.String', [], validators, data)


# TODO: rest of supported schema types


default_marshmallow_generators = {
    'string': marshmallow_string_generator
}
