import os

import pytest

from oarepo_model_builder.proxies import current_model_builder


class LiteEntryPoint:
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def load(self):
        return self.val


def extra_entrypoints(app, group=None, name=None):
    from . import datamodels

    data = {
        'oarepo_model_builder.datamodels': [
            LiteEntryPoint('test', datamodels),
        ],
    }

    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


@pytest.fixture()
def datamodel_json():
    return {
        "title": "Test record v1.0.0",
        "type": "object",
        "additionalProperties": False,
        # TODO: implement oarepo:include
        # "oarepo:include": ["invenio-record-v1.0.0"],
        "oarepo:ui": {
            "title": {
                "cs": "Datamodel title CS",
                "en": "Datamodel title EN"
            }
        },
        "properties": {
            "field1": {
                "type": "string",
                "oarepo:ui": {
                    "hint": {
                        "cs": "testovaci field",
                        "en": "test field"
                    },
                },
                "oarepo:search": {
                    "mapping": "keyword"
                },
            },
            "field2": {
                "type": "object",
                "description": "Record access control and ownership.",
                "additionalProperties": False,
                "properties": {
                    "subfield1": {
                        "description": "Sub field 1.",
                        "type": "array",
                        # TODO: implement items auto import
                        # "items": "rdm-definitions-v1.0.0#agent",
                        "oarepo:ui": {
                            "label": {"cs": "vloz subfield1 hodnotu",
                                      "en": "enter subfield1 value"}
                        }
                        # TODO: implement default mappings for field without `search` spec
                    }
                }
            }
        }
    }


@pytest.fixture()
def model_config():
    config = current_model_builder.model_config
    config.base_dir = os.getcwd()

    config.source = None
    config.package = (os.path.basename(os.getcwd())).replace('-', '_')
    config.kebab_package = config.package.replace('_', '-')
    config.datamodel = config.kebab_package
    config.datamodel_version = '1.0.0'
    return config
