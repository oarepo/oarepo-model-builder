from oarepo_model_builder.builders import MappingBuilder
from oarepo_model_builder.builders import BuildResult
from oarepo_model_builder.outputs import MappingOutput
from oarepo_model_builder.proxies import current_model_builder


def test_mapping_builder():
    mb = MappingBuilder()

    config = current_model_builder.model_config

    outputs = {}
    el = {}
    mb.begin(config, outputs, el)
    res = mb.pre(el, config, ['el'], outputs)

    assert res == BuildResult.KEEP
    assert len(outputs) == 1
    assert isinstance(outputs['mapping'], MappingOutput)

    test_cases = [
        # Test single field mapping
        (
            {'type': 'keyword'},
            ['properties', 'test1', 'search'],
            {
                'mappings': {
                    'properties': {
                        'test1': {'type': 'keyword'}
                    }
                }
            },
            BuildResult.DELETE
        ),
        # Test shorthand mapping specification
        (
            'keyword',
            ['properties', 'test2', 'search'],
            {
                'mappings': {
                    'properties': {
                        'test2': {'type': 'keyword'}
                    }
                }
            },
            BuildResult.DELETE
        )
    ]

    for tc in test_cases:
        outputs = {}
        config = {'mapping': {'initial': {}}}

        el, path, mapping, result = tc
        print(el, path)
        mb.begin(config, outputs, el)
        mb.pre(el, config, path, outputs)
        # res = mb.pre(el, config, path, outputs)
        # assert res == result TODO: remove this as KEEP/DELETE is not needed anymore
        assert outputs['mapping'].data == mapping
