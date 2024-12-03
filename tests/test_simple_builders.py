import os

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.invenio.edtf_interval_dumper import EDTFIntervalDumperBuilder
from oarepo_model_builder.invenio.invenio_api_views import InvenioAPIViewsBuilder
from oarepo_model_builder.invenio.invenio_config import InvenioConfigBuilder
from oarepo_model_builder.invenio.invenio_ext import InvenioExtBuilder
from oarepo_model_builder.invenio.invenio_proxies import InvenioProxiesBuilder
from oarepo_model_builder.invenio.invenio_record import InvenioRecordBuilder
from oarepo_model_builder.invenio.invenio_record_dumper import (
    InvenioRecordDumperBuilder,
)
from oarepo_model_builder.invenio.invenio_record_item import InvenioRecordItemBuilder
from oarepo_model_builder.invenio.invenio_record_list import InvenioRecordListBuilder
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
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.schema import ModelSchema

from .utils import strip_whitespaces


def build_python_model(model, output_builders, fn):
    builder = ModelBuilder(
        output_builders=output_builders,
        outputs=[PythonOutput],
        filesystem=InMemoryFileSystem(),
    )
    builder.build(
        model=ModelSchema(
            "",
            {
                "settings": {
                    "python": {
                        "use-isort": False,
                        "use-black": False,
                        "use-autoflake": False,
                    },
                    "opensearch": {"version": "os-v2"},
                },
                "record": {"module": {"qualified": "test"}, **model},
            },
        ),
        profile="record",
        model_path=["record"],
        output_dir="",
    )

    return builder.filesystem.read(fn)


def test_record_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordBuilder],
        os.path.join("test", "records", "api.py"),  # NOSONAR
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField
from invenio_records_resources.records.systemfields.pid import PIDFieldContext
from test.records.models import TestMetadata
from test.records.dumpers.dumper import TestDumper
from invenio_records_resources.records.api import Record as InvenioRecord
class TestRecord(InvenioRecord):
    model_cls = TestMetadata
    schema = ConstantField("$schema", "local://test-1.0.0.json")
    index = IndexField("test-test-1.0.0",)
    pid = PIDField(
        provider=TestIdProvider,
        context_cls=PIDFieldContext,
        create=True
    
    )
    dumper = TestDumper()
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
from test.records.models import TestMetadata
from test.records.dumpers.dumper import TestDumper
from invenio_records_resources.records.api import Record as InvenioRecord

class TestIdProvider(RecordIdProviderV2):
    pid_type = "test"

class TestRecord(InvenioRecord):
    model_cls = TestMetadata
    schema = ConstantField("$schema", "local://test-1.0.0.json")
    index = IndexField("test-test-1.0.0",)
    pid = PIDField(
        provider=TestIdProvider,
        context_cls=PIDFieldContext,
        create=True
    
    )
    dumper = TestDumper()
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
from test import config


class TestExt:

    def __init__(self, app=None):
        
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.app = app
        
        self.init_config(app)
        if not self.is_inherited():
            self.register_flask_extension(app)

    def register_flask_extension(self, app):
        
        app.extensions["test"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for identifier in dir(config):
            if re.match('^[A-Z_0-9]*$', identifier) and not identifier.startswith('_'):
                if isinstance(app.config.get(identifier), list):
                    app.config[identifier]+= getattr(config, identifier)
                elif isinstance(app.config.get(identifier), dict):
                    for k, v in getattr(config, identifier).items():
                        if k not in app.config[identifier]:
                            app.config[identifier][k]= v                
                else:
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

current_service = _ext_proxy('service_records')
"""Proxy to the instantiated service."""

current_resource = _ext_proxy('resource_records')
"""Proxy to the instantiated resource."""
        '''
    )


def test_config_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioConfigBuilder],
        os.path.join("test", "config.py"),  # NOSONAR
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        """
from test.services.records.config import TestServiceConfig
from test.services.records.service import TestService
from test.resources.records.config import TestResourceConfig
from test.resources.records.resource import TestResource
from test.records.api import TestRecord


TEST_RECORD_RESOURCE_CONFIG = TestResourceConfig
TEST_RECORD_RESOURCE_CLASS = TestResource
TEST_RECORD_SERVICE_CONFIG = TestServiceConfig
TEST_RECORD_SERVICE_CLASS = TestService
OAREPO_PRIMARY_RECORD_SERVICE={
   TestRecord: "test"
}
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

    blueprint_name = 'test'
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

class TestService(InvenioRecordService):
    """TestRecord service."""        
'''
    )


def test_service_config():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordServiceConfigBuilder],
        os.path.join("test", "services", "records", "config.py"),
    )
    print(data)
    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from invenio_records_resources.services import RecordServiceConfig as InvenioRecordServiceConfig
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import pagination_links
from test.records.api import TestRecord
from test.services.records.permissions import TestPermissionPolicy
from test.services.records.schema import TestSchema
from test.services.records.search import TestSearchOptions
from test.services.records.results import TestRecordItem
from test.services.records.results import TestRecordList

from oarepo_runtime.services.components import process_service_configs

class TestServiceConfig(PermissionsPresetsConfigMixin, InvenioRecordServiceConfig):
    """TestRecord service config."""
    result_item_cls = TestRecordItem
    result_list_cls = TestRecordList
    PERMISSIONS_PRESETS = ["everyone"]
    url_prefix = "/test/"
    base_permission_policy_cls = TestPermissionPolicy
    schema = TestSchema
    search = TestSearchOptions
    record_cls = TestRecord
    service_id = "test"
    @property
    def components(self):
        components_list = []
        components_list.extend(process_service_configs(type(self).mro()[2:]))
        additional_components = []
        components_list.extend(additional_components)
        return components_list
    model = "test"
    
    @property
    def links_item(self):
        return {
            
            "self":RecordLink("{+api}/test/{id}"),
            
            "self_html":RecordLink("{+ui}/test/{id}"),
            
        }
    @property
    def links_search(self):
        return {
            
            **pagination_links("{+api}/test/{?args*}"),
            
        }
'''
    )


def test_api_views_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioAPIViewsBuilder],
        os.path.join("test", "views", "records", "api.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from flask import Blueprint

def create_api_blueprint(app):
    """Create TestRecord blueprint."""
    blueprint = app.extensions["test"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    #calls record_once for all other functions starting with "init_addons_"
    #https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [v for k, v in funcs.items() if k.startswith("init_addons_test") and callable(v)]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint

def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["test"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.service_records, service_id=ext.service_records.config.service_id)

    # Register indexer
    if hasattr(ext.service_records, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(ext.service_records.indexer, indexer_id=ext.service_records.config.service_id)
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
# from invenio_records_permissions.generators import SystemProcess, AnyUser

class TestPermissionPolicy(RecordPermissionPolicy):
    """test.records.api.TestRecord permissions.
        Values in this class will be merged with permission presets.
    """
    can_search = []
    can_read = []
    can_create = []
    can_update = []
    can_delete = []
    can_manage = []
    can_read_files=[]
    can_update_files=[]
'''
    )


def test_dumper_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordDumperBuilder],
        os.path.join("test", "records", "dumpers", "dumper.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from oarepo_runtime.records.dumpers import SearchDumper
from test.records.dumpers.edtf import TestEDTFIntervalDumperExt

class TestDumper(SearchDumper):
    """TestRecord opensearch dumper."""
    extensions=[ TestEDTFIntervalDumperExt()]
'''
    )


def test_edtf_interval_dumper_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "edtf-interval"}}},
        [EDTFIntervalDumperBuilder],
        os.path.join("test", "records", "dumpers", "edtf.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from oarepo_runtime.records.dumpers.edtf_interval import EDTFIntervalDumperExt
class TestEDTFIntervalDumperExt(EDTFIntervalDumperExt):
    """edtf interval dumper."""
    paths=['a']
        '''
    )


def test_ui_serializer_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordUISerializerBuilder],
        os.path.join("test", "resources", "records", "ui.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from oarepo_runtime.resources import LocalizedUIJSONSerializer

from test.services.records.ui_schema import TestUISchema
from flask_resources.serializers import JSONSerializer
from flask_resources import BaseListSchema
from flask import g

class TestUIJSONSerializer(LocalizedUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=TestUISchema,
            list_schema_cls=BaseListSchema,
            schema_context={ "object_key": "ui", "identity": g.identity }
        )
'''
    )


def test_record_item_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordItemBuilder],
        os.path.join("test", "services", "records", "results.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from oarepo_runtime.services.results import RecordItem
 class TestRecordItem(RecordItem):
 """TestRecord record item."""
 components=[*RecordItem.components]
        '''
    )


def test_record_list_builder():
    data = build_python_model(
        {"properties": {"a": {"type": "keyword"}}},
        [InvenioRecordListBuilder],
        os.path.join("test", "services", "records", "results.py"),
    )

    assert strip_whitespaces(data) == strip_whitespaces(
        '''
from oarepo_runtime.services.results import RecordList
 class TestRecordList(RecordList):
 """TestRecord record list."""
 components=[*RecordList.components]
        '''
    )
