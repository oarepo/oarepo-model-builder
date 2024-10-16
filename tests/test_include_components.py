import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

from .utils import strip_whitespaces

OAREPO_USE = "use"



def test_include_invenio():
    schema = load_model(
        "test.yaml",  # NOSONAR
        model_content={
            "version": "1.0.0",

            "record": {
                "module": {"qualified": "test"},
                OAREPO_USE: ["invenio", "doi", "oaipmh"],
                "properties": {"a": {"type": "keyword", "required": True}},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "config.py")
    ).read()
    data = str(data)
    assert "components=[*PermissionsPresetsConfigMixin.components,*InvenioRecordServiceConfig.components,DoiComponent,OaiSectionComponent]" in re.sub(r"\s", "", data)