import functools

from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.stack import ModelBuilderStack, ModelBuilderStackEntry


def test_stack():
    schema = ModelSchema('', {
        'a': {
            'b': [1, 2],
            'c': 3
        },
        'd': 4,
        'e': {
            'f': 5
        }
    })
    stack = ModelBuilderStack(schema)
    out = []

    def on_data(stack):
        if stack.top_type != stack.PRIMITIVE:
            out.append(('enter', stack.top, stack.level))
            yield
            out.append(('leave', stack.top, stack.level))
        else:
            out.append(('primitive', stack.top, stack.level))

    stack.process(on_data)

    assert out == [
        ('enter', ModelBuilderStackEntry(key=None, data={'a': {'b': [1, 2], 'c': 3}, 'd': 4, 'e': {'f': 5}}), 1),
        ('enter', ModelBuilderStackEntry(key='a', data={'b': [1, 2], 'c': 3}), 2),
        ('enter', ModelBuilderStackEntry(key='b', data=[1, 2]), 3),
        ('primitive', ModelBuilderStackEntry(key=0, data=1), 4),
        ('primitive', ModelBuilderStackEntry(key=1, data=2), 4),
        ('leave', ModelBuilderStackEntry(key='b', data=[1, 2]), 3),
        ('primitive', ModelBuilderStackEntry(key='c', data=3), 3),
        ('leave', ModelBuilderStackEntry(key='a', data={'b': [1, 2], 'c': 3}), 2),
        ('primitive', ModelBuilderStackEntry(key='d', data=4), 2),
        ('enter', ModelBuilderStackEntry(key='e', data={'f': 5}), 2),
        ('primitive', ModelBuilderStackEntry(key='f', data=5), 3),
        ('leave', ModelBuilderStackEntry(key='e', data={'f': 5}), 2),
        ('leave', ModelBuilderStackEntry(key=None, data={'a': {'b': [1, 2], 'c': 3}, 'd': 4, 'e': {'f': 5}}), 1)
    ]
