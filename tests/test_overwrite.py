import shutil
from tempfile import mkdtemp

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import FileSystem

OAREPO_USE = "use"


def test_overwrite():
    schema = load_model(
        "test.yaml",
        model_content={
            "version": "1.0.0",
            "record": {OAREPO_USE: "invenio", "properties": {"a": {"type": "keyword"}}},
        },
        isort=False,
        black=False,
    )

    filesystem = FileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem, overwrite=True)

    tmpdir = mkdtemp()
    try:
        builder.build(schema, "record", ["record"], tmpdir)
    finally:
        shutil.rmtree(tmpdir)
