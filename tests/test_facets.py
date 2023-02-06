import json
import os
import re
from io import StringIO
from pathlib import Path
from typing import Dict

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

DUMMY_YAML = "test.yaml"

def test_include_invenio():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "a":  "fulltext+keyword",
                    "b": {
                        "type": "keyword",
                        "facets": {"field": 'TermsFacet(field="cosi")'},
                    },
                },
            },
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "facets.py")
    ).read()
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



a_keyword = TermsFacet(field = "a.keyword")



b = TermsFacet(field="cosi")



_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
    """,
    )

def test_nested():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "b": {
                        "type": "nested",
                        "properties": {
                            "c": {
                                "type": "keyword",
                            },
                            "d": {"type": "fulltext+keyword"},
                            "f": {
                                "type" : "nested",
                                "properties": {"g": {"type": "keyword"}},

                            },
                        }
                    }
                },
            },
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "facets.py")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet




b_c = NestedLabeledFacet(path =" b", nested_facet = TermsFacet(field = "b.c"))



b_d_keyword = NestedLabeledFacet(path =" b", nested_facet=TermsFacet(field = "b.d.keyword"))




b_f_g = NestedLabeledFacet(path =" b", nested_facet=NestedLabeledFacet(path =" b.f", nested_facet=TermsFacet(field = "b.f.g")))



_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
    
""",)
def test_object():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "b": {
                        "type": "object",
                        "properties": {
                            "c": {
                                "type": "keyword",
                            },
                            "d": {"type": "fulltext+keyword"},
                            "f": {
                                "type" : "object",
                                "properties": {"g": {"type": "keyword"}},

                            },
                        }
                    }
                },
            },
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "facets.py")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
        \"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet




b_c = TermsFacet(field = "b.c")



b_d_keyword = TermsFacet(field = "b.d.keyword")



b_f_g = TermsFacet(field = "b.f.g")



_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
""",
    )

def test_nest_obj():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "b_nes": {
                        "type": "object",
                        "properties": {
                            "c": {
                                "type": "keyword",
                            },
                            "d": {"type": "fulltext+keyword"},
                            "f": {
                                "type" : "object",
                                "properties": {"g": {"type": "keyword"}},

                            },
                        }
                    },
                    "b_obj": {
                        "type": "object",
                        "properties": {
                            "c": {
                                "type": "keyword",
                            },
                            "d": {"type": "fulltext+keyword"},
                            "f": {
                                "type": "nested",
                                "properties": {"g": {"type": "keyword"}},

                            },
                        }
                    }
                },
            },
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "facets.py")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
        \"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet




b-nes_c = NestedLabeledFacet(path =" b", nested_facet=TermsFacet(field = "b-nes.c"))



b-nes_d_keyword = NestedLabeledFacet(path =" b", nested_facet=TermsFacet(field = "b-nes.d.keyword"))



b-nes_f_g = NestedLabeledFacet(path =" b", nested_facet=TermsFacet(field = "b-nes.f.g"))



b-obj_c = TermsFacet(field = "b-obj.c")



b-obj_d_keyword = TermsFacet(field = "b-obj.d.keyword")


#???????????????????????????????????????????#
b-obj_f_g = TermsFacet(field = "b-obj.f.g")



_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
""",
    )
