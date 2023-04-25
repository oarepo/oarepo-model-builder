import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.invenio_config import InvenioConfigBuilder
from oarepo_model_builder.invenio.invenio_ext import InvenioExtBuilder
from oarepo_model_builder.invenio.invenio_proxies import InvenioProxiesBuilder
from oarepo_model_builder.invenio.invenio_record import InvenioRecordBuilder
from oarepo_model_builder.invenio.invenio_record_dumper import (
    InvenioRecordDumperBuilder,
)
from oarepo_model_builder.invenio.invenio_record_metadata import (
    InvenioRecordMetadataBuilder,
)
from oarepo_model_builder.invenio.invenio_record_permissions import (
    InvenioRecordPermissionsBuilder,
)
from oarepo_model_builder.invenio.invenio_record_pid_provider import (
    InvenioRecordPIDProviderBuilder,
)
from oarepo_model_builder.invenio.invenio_record_resource import (
    InvenioRecordResourceBuilder,
)
from oarepo_model_builder.invenio.invenio_record_resource_config import (
    InvenioRecordResourceConfigBuilder,
)
from oarepo_model_builder.invenio.invenio_record_service import (
    InvenioRecordServiceBuilder,
)
from oarepo_model_builder.invenio.invenio_record_service_config import (
    InvenioRecordServiceConfigBuilder,
)
from oarepo_model_builder.invenio.invenio_record_ui_serializer import (
    InvenioRecordUISerializerBuilder,
)
from oarepo_model_builder.invenio.invenio_version import InvenioVersionBuilder
from oarepo_model_builder.invenio.invenio_views import InvenioViewsBuilder
from oarepo_model_builder.model_preprocessors.default_values import (
    DefaultValuesModelPreprocessor,
)
from oarepo_model_builder.model_preprocessors.invenio import InvenioModelPreprocessor
from oarepo_model_builder.model_preprocessors.invenio_base_classes import (
    InvenioBaseClassesModelPreprocessor,
)
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema

from .utils import strip_whitespaces


def build_python_model(model, output_builders, fn):
    builder = ModelBuilder(
        output_builders=output_builders,
        outputs=[PythonOutput],
        model_preprocessors=[
            DefaultValuesModelPreprocessor,
            InvenioModelPreprocessor,
            InvenioBaseClassesModelPreprocessor,
        ],
        filesystem=InMemoryFileSystem(),
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "schema-version": "1.0.0",
                    "python": {
                        "use-isort": False,
                        "use-black": False,
                        "use-autoflake": False,
                    },
                    "opensearch": {"version": "os-v2"},
                },
                "model": {"package": "test", **model},
            },
        ),
        output_dir="",
    )

    return builder.filesystem.read(fn)


def test_record_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordBuilder],
        os.path.join("test", "records", "api.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.systemfields import IndexField
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records_resources.records.systemfields.pid import PIDField
from invenio_records_resources.records.systemfields.pid import PIDFieldContext
from invenio_records_resources.records.api import Record
from test.records.models import TestMetadata
from test.records.dumper import TestDumper

class TestRecord(Record):
    model_cls = TestMetadata
    schema = ConstantField("$schema", "local://test-1.0.0.json")
    index = IndexField("test-test-1.0.0")
    pid = PIDField(
        provider=TestIdProvider,
        context_cls=PIDFieldContext,
        create=True
    
    )
    dumper_extensions = []
    dumper = TestDumper(extensions=dumper_extensions)
"""
    )


def test_record_pid_provider_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [
            InvenioRecordPIDProviderBuilder,
            InvenioRecordBuilder,
        ],
        os.path.join("test", "records", "api.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.systemfields import IndexField

from invenio_records_resources.records.systemfields.pid import PIDField
from invenio_records_resources.records.systemfields.pid import PIDFieldContext

from invenio_records_resources.records.api import Record

from test.records.models import TestMetadata
from test.records.dumper import TestDumper


class TestIdProvider(RecordIdProviderV2 ):
    pid_type = "test"

class TestRecord(Record ):
    model_cls = TestMetadata

    schema = ConstantField("$schema", "local://test-1.0.0.json")


    index = IndexField("test-test-1.0.0")


    pid = PIDField(
        provider=TestIdProvider,
        context_cls=PIDFieldContext,
        create=True
    
    )

    dumper_extensions = []
    dumper = TestDumper(extensions=dumper_extensions)

"""
    )


def test_record_metadata_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [
            InvenioRecordMetadataBuilder,
        ],
        os.path.join("test", "records", "models.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_db import db


from invenio_records.models import RecordMetadataBase


class TestMetadata(db.Model, RecordMetadataBase):
    """Model for TestRecord metadata."""

    __tablename__ = "test_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
'''
    )


def test_ext_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioExtBuilder],
        os.path.join("test", "ext.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
import re
from test import config as config


class TestExt():
    """test extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.resource = None
        self.service = None
        
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        
        self.init_config(app)
        if not self.is_inherited():
            self.init_resource(app)
            self.register_flask_extension(app)

    def register_flask_extension(self, app):
        
        app.extensions["test"] = self

    def init_resource(self, app):
        """Initialize vocabulary resources."""
        self.service = app.config["TEST_SERVICE_CLASS_TEST"](
            config=app.config["TEST_SERVICE_CONFIG_TEST"](),
        )
        self.resource = app.config["TEST_RESOURCE_CLASS_TEST"](
            service=self.service,
            config=app.config["TEST_RESOURCE_CONFIG_TEST"](),
        )

    def init_config(self, app):
        """Initialize configuration."""
        for identifier in dir(config):
            if re.match('^[A-Z_0-9]*$', identifier) and not identifier.startswith('_'):
                app.config.setdefault(identifier, getattr(config, identifier))

    def is_inherited(self):
        from importlib_metadata import entry_points

        ext_class = type(self)
        for ep in entry_points(group='invenio_base.apps'):
            loaded = ep.load()
            if loaded is not ext_class and issubclass(ext_class, loaded):
                return True
        for ep in entry_points(group='invenio_base.api_apps'):
            loaded = ep.load()
            if loaded is not ext_class and issubclass(ext_class, loaded):
                return True
        return False
'''
    )


def test_proxies_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioProxiesBuilder],
        os.path.join("test", "proxies.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from flask import current_app
from werkzeug.local import LocalProxy

def _ext_proxy(attr):
    return LocalProxy(
        lambda: getattr(current_app.extensions["test"], attr))

current_service = _ext_proxy('service')
"""Proxy to the instantiated vocabulary service."""

current_resource = _ext_proxy('resource')
"""Proxy to the instantiated vocabulary resource."""
        '''
    )


def test_config_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioConfigBuilder],
        os.path.join("test", "config.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
from test.services.records.config import TestServiceConfig
from test.services.records.service import TestService
from test.resources.records.config import TestResourceConfig
from test.resources.records.resource import TestResource


TEST_RESOURCE_CONFIG_TEST = TestResourceConfig
TEST_RESOURCE_CLASS_TEST = TestResource
TEST_SERVICE_CONFIG_TEST = TestServiceConfig
TEST_SERVICE_CLASS_TEST = TestService
        """
    )


def test_version_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioVersionBuilder],
        os.path.join("test", "version.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
__version__ = "1.0.0"
        """
    )


def test_resource_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordResourceBuilder],
        os.path.join("test", "resources", "records", "resource.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_records_resources.resources import RecordResource
class TestResource(RecordResource):
    """TestRecord resource."""
    # here you can for example redefine
    # create_url_rules function to add your own rules
        '''
    )


def test_resource_config_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordResourceConfigBuilder],
        os.path.join("test", "resources", "records", "config.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
import importlib_metadata
from flask_resources import ResponseHandler

from test.resources.records.ui import TestUIJSONSerializer
from invenio_records_resources.resources import RecordResourceConfig

class TestResourceConfig(RecordResourceConfig):
    """TestRecord resource config."""

    blueprint_name = 'Test'
    url_prefix = '/test/'

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(group='invenio.test.response_handlers'):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(TestUIJSONSerializer()),
            **super().response_handlers,
            **entrypoint_response_handlers
        }
        '''
    )


def test_service_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordServiceBuilder],
        os.path.join("test", "services", "records", "service.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_records_resources.services import RecordService as InvenioRecordService
from invenio_records_resources.services import RecordService

class TestService(RecordService):
    """TestRecord service."""        
'''
    )


def test_service_config():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordServiceConfigBuilder],
        os.path.join("test", "services", "records", "config.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_records_resources.services import RecordServiceConfig as InvenioRecordServiceConfig
from invenio_records_resources.services import RecordLink, pagination_links
from invenio_records_resources.services import RecordServiceConfig
from oarepo_runtime.relations.components import CachingRelationsComponent
from test.records.api import TestRecord
from test.services.records.permissions import TestPermissionPolicy
from test.services.records.schema import TestSchema
from test.services.records.search import TestSearchOptions

class TestServiceConfig(RecordServiceConfig):
    """TestRecord service config."""
    url_prefix = "/test/"
    
    permission_policy_cls = TestPermissionPolicy
    
    schema = TestSchema
    
    search = TestSearchOptions
    
    record_cls = TestRecord
    service_id = "test"
    
    components = [ *RecordServiceConfig.components, CachingRelationsComponent   ]

    model = "test"
    
    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

'''
    )


def test_views_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioViewsBuilder],
        os.path.join("test", "views.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from flask import Blueprint

def create_blueprint_from_app_test(app):
    """Create test blueprint."""
    blueprint = app.extensions["test"].resource.as_blueprint()
    blueprint.record_once(init_create_blueprint_from_app_test)

    #calls record_once for all other functions starting with "init_addons_"
    #https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [v for k, v in funcs.items() if k.startswith("init_addons_test") and callable(v)]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint

def init_create_blueprint_from_app_test(state):
    """Init app."""
    app = state.app
    ext = app.extensions["test"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.service, service_id="test")

    # Register indexer
    if hasattr(ext.service, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(ext.service.indexer, indexer_id="test")

def create_blueprint_from_app_testExt(app):
    """Create test-ext blueprint."""
    blueprint = Blueprint(
        'test-ext',
        __name__,
        url_prefix='test')
    blueprint.record_once(init_create_blueprint_from_app_test)

    #calls record_once for all other functions starting with "init_app_addons_"
    #https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [v for k, v in funcs.items() if k.startswith("init_app_addons_test") and callable(v)]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


        '''
    )


def test_permissions_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordPermissionsBuilder],
        os.path.join("test", "services", "records", "permissions.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import SystemProcess, AnyUser


class TestPermissionPolicy(RecordPermissionPolicy):
    """test.records.api.TestRecord permissions."""

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AnyUser()]
    can_create = [SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]
    can_manage = [SystemProcess()]
'''
    )


def test_dumper_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordDumperBuilder],
        os.path.join("test", "records", "dumper.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_records.dumpers import SearchDumper

class TestDumper(SearchDumper):
    """TestRecord opensearch dumper."""
'''
    )


def test_ui_serializer_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordUISerializerBuilder],
        os.path.join("test", "records", "dumper.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_records.dumpers import SearchDumper

class TestDumper(SearchDumper):
    """TestRecord opensearch dumper."""
'''
    )