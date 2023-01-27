import json
import os
import re
from io import StringIO
from pathlib import Path
from typing import Dict

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import AbstractFileSystem

# from tests.mock_filesystem import MockFilesystem


class MockFilesystem(AbstractFileSystem):
    def __init__(self):
        self.files: Dict[str, StringIO] = {}

    def open(self, path: str, mode: str = "r"):
        path = Path(path).absolute()
        if mode == "r":
            if not path in self.files:
                raise FileNotFoundError(
                    f"File {path} not found. Known files {[f for f in self.files]}"
                )
            return StringIO(self.files[path].getvalue())
        self.files[path] = StringIO()
        self.files[path].close = lambda: None
        return self.files[path]

    def exists(self, path):
        path = Path(path).absolute()
        return path in self.files

    def mkdir(self, path):
        pass

    def snapshot(self):
        ret = {}
        for fname, io in self.files.items():
            ret[fname] = io.getvalue()
        return ret

def remove_whitespaces(str):
    return re.sub(r"\s", "", str)

def is_in(str1, str2):
    return remove_whitespaces(str1) in remove_whitespaces(str2)

def update_dict(dct, upd):
    return dict(dct, **upd)

MODEL_BASE = {

    "model": {
        "properties": {
            "file": {"type": "fulltext+keyword"},
            "b": {
                "type": "keyword",
                "facets": {"field": 'TermsFacet(field="cosi")'},
            },
        },
        "use": "invenio",
    },
}

MODEL_2_EXPANDABLE_FIELD = {
    "field-name": "metadata.file",
    "referenced-keys": [
        "metadata.filename",
        "metadata.filesize"
    ],
    "service": "model_file.proxies.current_service"
}

MODEL_1_EXPANDABLE_FIELD = {
    "field-name": "metadata.picture",
    "referenced-keys": [
        "metadata.alt"
    ],
    "service": "model_picture.proxies.current_service"
}

MODEL_EXPANDABLE_FIELD_SERVICE_ALIAS = update_dict(MODEL_1_EXPANDABLE_FIELD, {"service-alias": "big_pic_service"})
MODEL_EXPANDABLE_FIELD_PID_FIELD = update_dict(MODEL_1_EXPANDABLE_FIELD, {"pid_field": "alt_id"})
MODEL_EXPANDABLE_FIELD_CUSTOM_CLASS = update_dict(MODEL_1_EXPANDABLE_FIELD, {"expandable-field-class": "test_classes.InheritedReferencedRecordExpandableField"})


IMPORT_CONFIGMIXIN = "from oarepo_records_resources.services.service import ExpandableFieldsConfigMixin"
IMPORT_SERVICE_1 = "from model_picture.proxies import current_service as picture_service"
IMPORT_SERVICE_2 = "from model_file.proxies import current_service as file_service"
IMPORT_SERVICE_1_ALIAS = "from model_picture.proxies import current_service as big_pic_service"
IMPORT_DEFAULT_FIELD = "from oarepo_records_resources.services.expandable_fields import ReferencedRecordExpandableField"
IMPORT_CUSTOM_FIELD = "from test_classes import InheritedReferencedRecordExpandableField"

SERVICE_WITH_FIELDS = "class TestService(ExpandableFieldsConfigMixin,RecordService):"
SERVICE_WITHOUT_FIELDS = "class TestService(RecordService):"

CONFIG_PATH = os.path.join("test", "services", "records", "config.py")
SERVICE_PATH = os.path.join("test", "services", "records", "service.py")

EXPANDABLE_FIELD = """
    @property
    def expandable_fields(self):
        return [
            ReferencedRecordExpandableField(
                field_name="metadata.picture",
                keys=['metadata.alt'],
                service=picture_service
            ),
        ]
"""
EXPANDABLE_FIELD_SERVICE_ALIAS = """
    @property
    def expandable_fields(self):
        return [
            ReferencedRecordExpandableField(
                field_name="metadata.picture",
                keys=['metadata.alt'],
                service=big_pic_service
            ),
        ]
"""
EXPANDABLE_FIELD_PID_ID = """
    @property
    def expandable_fields(self):
        return [
            ReferencedRecordExpandableField(
                field_name="metadata.picture",
                keys=['metadata.alt'],
                service=picture_service,
                pid_field="alt_id"
            ),
        ]
"""
EXPANDABLE_FIELD_CUSTOM_CLASS = """
    @property
    def expandable_fields(self):
        return [
            InheritedReferencedRecordExpandableField(
                field_name="metadata.picture",
                keys=['metadata.alt'],
                service=picture_service
            ),
        ]
"""

EXPANDABLE_FIELDS_TWO = """
    @property
    def expandable_fields(self):
        return [
            ReferencedRecordExpandableField(
                field_name="metadata.picture",
                keys=['metadata.alt'],
                service=picture_service
            ),
            ReferencedRecordExpandableField(
                field_name="metadata.file",
                keys=['metadata.filename', 'metadata.filesize'],
                service=file_service
            ),
        ]
"""

def basic_test_template(expandable_fields_def, is_in_conditions):
    model = MODEL_BASE
    model = update_dict(model, {"expandable-fields": expandable_fields_def})
    schema = load_model(
        "test.yaml",
        "test",
        model_content=model,
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    config = builder.filesystem.open(CONFIG_PATH).read()
    service = builder.filesystem.open(SERVICE_PATH).read()
    for condition in is_in_conditions:
        if condition[1] == "service":
            assert is_in(condition[0], service)
        elif condition[1] == "config":
            assert is_in(condition[0], config)
        else:
            raise ValueError


def test_no_expandable_fields():
    schema = load_model(
        "test.yaml",
        "test",
        model_content=MODEL_BASE,
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    config = builder.filesystem.open(CONFIG_PATH).read()
    service = builder.filesystem.open(SERVICE_PATH).read()

    assert remove_whitespaces(IMPORT_CONFIGMIXIN) not in remove_whitespaces(service)
    assert remove_whitespaces(SERVICE_WITHOUT_FIELDS) in remove_whitespaces(service)
    print()


def test_single_expandable_field():
    conditions = (
        (IMPORT_CONFIGMIXIN, "service"),
        (SERVICE_WITH_FIELDS, "service"),
        (EXPANDABLE_FIELD, "config"),
        (IMPORT_SERVICE_1, "config"),
        (IMPORT_DEFAULT_FIELD, "config")

    )
    basic_test_template([MODEL_1_EXPANDABLE_FIELD], conditions)


def test_service_alias():
    conditions = (
        (IMPORT_CONFIGMIXIN, "service"),
        (SERVICE_WITH_FIELDS, "service"),
        (EXPANDABLE_FIELD_SERVICE_ALIAS, "config"),
        (IMPORT_SERVICE_1_ALIAS, "config"),
        (IMPORT_DEFAULT_FIELD, "config")

    )
    basic_test_template([MODEL_EXPANDABLE_FIELD_SERVICE_ALIAS], conditions)

def test_service_pid_field():
    conditions = (
        (IMPORT_CONFIGMIXIN, "service"),
        (SERVICE_WITH_FIELDS, "service"),
        (EXPANDABLE_FIELD_PID_ID, "config"),
        (IMPORT_SERVICE_1, "config"),
        (IMPORT_DEFAULT_FIELD, "config")

    )
    basic_test_template([MODEL_EXPANDABLE_FIELD_PID_FIELD], conditions)


def test_expandable_fields_custom_class():
    conditions = (
        (IMPORT_CONFIGMIXIN, "service"),
        (SERVICE_WITH_FIELDS, "service"),
        (EXPANDABLE_FIELD_CUSTOM_CLASS, "config"),
        (IMPORT_SERVICE_1, "config"),
        (IMPORT_CUSTOM_FIELD, "config")

    )
    basic_test_template([MODEL_EXPANDABLE_FIELD_CUSTOM_CLASS], conditions)

def test_two_expandable_fields():
    conditions = (
        (IMPORT_CONFIGMIXIN, "service"),
        (SERVICE_WITH_FIELDS, "service"),
        (EXPANDABLE_FIELDS_TWO, "config"),
        (IMPORT_SERVICE_1, "config"),
        (IMPORT_SERVICE_2, "config"),
        (IMPORT_DEFAULT_FIELD, "config")

    )
    basic_test_template([MODEL_1_EXPANDABLE_FIELD, MODEL_2_EXPANDABLE_FIELD], conditions)
