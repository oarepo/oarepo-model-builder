import os
import shutil
import tempfile

import pytest
from flask import Flask
from invenio_base.signals import app_loaded
from invenio_indexer.ext import InvenioIndexer
from invenio_jsonschemas.ext import InvenioJSONSchemas
from invenio_pidstore.ext import InvenioPIDStore
from invenio_records.ext import InvenioRecords
from invenio_records_rest.ext import InvenioRecordsREST
from invenio_search.ext import InvenioSearch

from oarepo_model_builder.ext import OARepoModelBuilder
from oarepo_model_builder.proxies import current_model_builder


@pytest.yield_fixture(scope="module")
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        JSONSCHEMAS_HOST="test.cz",
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SERVER_NAME='127.0.0.1:5000',
        INVENIO_INSTANCE_PATH=instance_path,
        DEBUG=True,
        # in tests, api is not on /api but directly in the root
        PIDSTORE_RECID_FIELD='pid',
        FLASK_TAXONOMIES_URL_PREFIX='/2.0/taxonomies/',
        # RECORDS_REST_ENDPOINTS=RECORDS_REST_ENDPOINTS,
        CELERY_BROKER_URL='amqp://guest:guest@localhost:5672//',
        CELERY_TASK_ALWAYS_EAGER=True,
        CELERY_RESULT_BACKEND='cache',
        CELERY_CACHE_BACKEND='memory',
        CELERY_TASK_EAGER_PROPAGATES=True,
        SUPPORTED_LANGUAGES=["cs", "en"],
        # RECORDS_REST_ENDPOINTS=RECORDS_REST_ENDPOINTS,
        ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE={
            "type": "text",
            "fields": {
                "keywords": {
                    "type": "keyword"
                }
            }
        },
    )

    app.secret_key = 'changeme'
    print(os.environ.get("INVENIO_INSTANCE_PATH"))

    InvenioJSONSchemas(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    InvenioRecords(app)
    InvenioRecordsREST(app)
    InvenioPIDStore(app)
    OARepoModelBuilder(app)

    # Celery
    print(app.config["CELERY_BROKER_URL"])

    # app.extensions['invenio-search'].mappings["test"] = mapping
    # app.extensions["invenio-jsonschemas"].schemas["test"] = schema

    app_loaded.send(app, app=app)

    with app.app_context():
        # app.register_blueprint(taxonomies_blueprint)
        print(app.url_map)
        yield app

    shutil.rmtree(instance_path)


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
def model_config(app):
    config = current_model_builder.model_config
    config.base_dir = os.getcwd()

    config.source = None
    config.package = (os.path.basename(os.getcwd())).replace('-', '_')
    config.kebab_package = config.package.replace('_', '-')
    config.datamodel = config.kebab_package
    config.datamodel_version = '1.0.0'
    return config
