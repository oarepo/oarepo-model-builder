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
                "properties": {
                    "a": {"type": "keyword", "required": True},
                    "harvest": {
                        "properties": {
                            "identifier": {
                                "type": "keyword",
                                "required": True
                            },
                            "datestamp": {
                                "type": "keyword",
                                "required": True
                            },
                        }
                    },
                },
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
    # print(data)

    data = re.sub(r"\s", "", str(data))

    assert "process_service_configs(self,DoiComponent,OaiSectionComponent)" in data
