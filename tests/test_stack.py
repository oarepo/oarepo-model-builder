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

    def on_data(event, stack):
        out.append((event, stack.top, stack.level))

    stack.process(
        functools.partial(on_data, 'enter'),
        functools.partial(on_data, 'leave'),
        functools.partial(on_data, 'primitive')
    )

    assert out == [
        ('enter', ModelBuilderStackEntry(key=None, el={'a': {'b': [1, 2], 'c': 3}, 'd': 4, 'e': {'f': 5}}), 1),
        ('enter', ModelBuilderStackEntry(key='a', el={'b': [1, 2], 'c': 3}), 2),
        ('enter', ModelBuilderStackEntry(key='b', el=[1, 2]), 3),
        ('primitive', ModelBuilderStackEntry(key=0, el=1), 4),
        ('primitive', ModelBuilderStackEntry(key=1, el=2), 4),
        ('leave', ModelBuilderStackEntry(key='b', el=[1, 2]), 3),
        ('primitive', ModelBuilderStackEntry(key='c', el=3), 3),
        ('leave', ModelBuilderStackEntry(key='a', el={'b': [1, 2], 'c': 3}), 2),
        ('primitive', ModelBuilderStackEntry(key='d', el=4), 2),
        ('enter', ModelBuilderStackEntry(key='e', el={'f': 5}), 2),
        ('primitive', ModelBuilderStackEntry(key='f', el=5), 3),
        ('leave', ModelBuilderStackEntry(key='e', el={'f': 5}), 2),
        ('leave', ModelBuilderStackEntry(key=None, el={'a': {'b': [1, 2], 'c': 3}, 'd': 4, 'e': {'f': 5}}), 1)
    ]
