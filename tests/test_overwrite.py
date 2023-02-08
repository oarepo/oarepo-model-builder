import json
import os
import re
import shutil
import sys
from pathlib import Path
from tempfile import mkdtemp, tempdir

from oarepo_model_builder.entrypoints import (create_builder_from_entrypoints,
                                              load_model)
from oarepo_model_builder.fs import FileSystem, InMemoryFileSystem
from tests.utils import assert_python_equals

OAREPO_USE = "use"


def test_overwrite():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "version": "1.0.0",
            "model": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = FileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem, overwrite=True)

    tmpdir = mkdtemp()
    try:
        builder.build(schema, tmpdir)
    finally:
        shutil.rmtree(tmpdir)
