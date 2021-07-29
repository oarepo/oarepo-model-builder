from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.builders.source import BuildResult, DataModelBuilder
from oarepo_model_builder.outputs.output import MappingOutput
from oarepo_model_builder.proxies import current_model_builder


def test_datamodel_builder(app, datamodel_json):
    build = DataModelBuilder()
    el_handlers = [MappingBuilder()]

    config = current_model_builder.model_config

    outputs = {}
    build(el=datamodel_json, config=config, path=[], outputs=outputs, handlers=el_handlers)

    assert len(outputs) == 1
    print(outputs['mapping'].data)


def test_mapping_builder(app):
    mb = MappingBuilder()

    config = current_model_builder.model_config

    outputs = {}
    res = mb.pre({}, config, [], outputs)

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
        el, path, mapping, result = tc
        print(el, path)
        mb.pre(el, {}, [], outputs)
        res = mb.pre(el, {}, path, outputs)
        assert res == result
        assert outputs['mapping'].data == mapping
