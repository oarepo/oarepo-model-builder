from oarepo_model_builder.builder import MappingBuilder, WalkResult, DataModelBuilder
from oarepo_model_builder.output import MappingOutput
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
    res = mb.pre({}, config, None, outputs)

    assert res == WalkResult.KEEP
    assert len(outputs) == 1
    assert isinstance(outputs['mapping'], MappingOutput)

    test_cases = [
        # Test single field mapping
        ({'type': 'keyword'}, ['test-record-v1.0.0', 'properties', 'test', 'search'], 'test', {'type': 'keyword'}),
        # Test shorthand mapping definition
        ('keyword', ['test-record-v1.0.0', 'properties', 'test', 'search'], 'test', {'type': 'keyword'})
    ]

    for tc in test_cases:
        source, path, field, result = tc

        res = mb.pre(source, config, path, outputs)
        if path[-1] == 'search':
            assert res == WalkResult.DELETE
        else:
            assert res == WalkResult.KEEP

        assert field in outputs['mapping'].data['mappings']['properties']
        assert outputs['mapping'].data['mappings']['properties'][field] == result
