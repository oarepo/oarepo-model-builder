import json
import os

from oarepo_model_builder import Config
from oarepo_model_builder.builders import DataModelBuilder
from oarepo_model_builder.builders import UIBuilder
from oarepo_model_builder.outputs.toml_output import toml_property
from oarepo_model_builder.proxies import current_model_builder


def test_ui_builder(model_config):
    builder = UIBuilder()
    test_path = '/tmp/test.json'
    test_pyproject_path = '/tmp/test.toml'
    outputs = {}

    # 1) Test that begin properly initializes outputs
    builder.begin(model_config, outputs, {})
    assert len(outputs) == 2
    assert outputs['ui'].path.split('/')[-3:] == [
        'oarepo_model_builder',
        'oarepo_ui',
        'oarepo-model-builder-v1.0.0.json'
    ]
    assert outputs['ui'].data == {**model_config.ui, 'fields': {}}
    assert len(builder.stack) == 2
    assert outputs['pyproject'].props_to_add == [
        toml_property(
            section='tool.poetry.plugins.oarepo_ui',
            property='oarepo-model-builder',
            value='oarepo_model_builder.oarepo_ui:oarepo-model-builder-v1.0.0.json'
        )]

    # 2) Test `pre` implementation

    # 2.1) `oarepo:` elements and subtrees are ignored by jsonschema
    src = {
        'oarepo:ui': {
            'title': {'cs': 'blah'}
        },
        'properties': {
            'test': {
                'oarepo:ui': {
                    'label': {
                        'cs': 'pole', 'en': 'field'
                    }}}}}
    b = DataModelBuilder()
    outputs = {}
    b(
        src,
        Config({
            **current_model_builder.model_config,
            'ui_path': test_path,
            'pyproject_path': test_pyproject_path,
            'base_dir': '/tmp'
        }),
        [], outputs, [
            UIBuilder()
        ])
    assert outputs['ui'].data == {
        'fields': {
            'test': {
                'label': {'cs': 'pole', 'en': 'field'}
            }}
        ,
        'title': {'cs': 'blah'}
    }
    assert outputs['ui'].output_type == 'ui'
    assert outputs['ui'].path == test_path
    outputs['ui'].save()

    with open(test_path, mode='r') as fp:
        saved = json.load(fp)
    os.remove(test_path)
    assert saved == outputs['ui'].data

    outputs['pyproject'].save()

    with open(test_pyproject_path, mode='r') as fp:
        saved = fp.read()
    # os.remove(test_pyproject_path)
    assert saved.strip() == """
["tool.poetry.plugins.oarepo_ui"]
oarepo-model-builder = "test.json"
""".strip()

