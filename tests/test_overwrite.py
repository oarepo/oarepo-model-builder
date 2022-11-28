import json
import os
import re
import shutil
import sys
from pathlib import Path
from tempfile import tempdir, mkdtemp

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import FileSystem
from tests.mock_filesystem import MockFilesystem
from tests.utils import assert_python_equals

OAREPO_USE = "oarepo:use"


def test_overwrite():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "version": "1.0.0",
            OAREPO_USE: "invenio",
            "model": {"properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = FileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    tmpdir = mkdtemp()
    try:
        builder.build(schema, tmpdir, overwrite=True)
    finally:
        shutil.rmtree(tmpdir)
