import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

DUMMY_YAML = "test.yaml"


def test_sort():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "a": {
                        "type": "fulltext+keyword",
                        "sortable": {"key": "a_test"},
                    },
                    "b": {
                        "type": "keyword",
                        "facets": {"field": 'TermsFacet(field="cosi")'},
                        "sortable": {"key": "b_test", "order": "desc"},
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
        os.path.join("test", "services", "records", "search.py")
    ).read()
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from . import facets

def _(x):
    \"""Identity function for string extraction.\"""
    return x

class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facets = {
    'a_keyword': facets.a_keyword,
    'b': facets.b,
    '_id': facets._id,
    'created': facets.created,
    'updated': facets.updated,
    '_schema': facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    'a_test': {'fields': ['a']},
    'b_test': {'fields': ['-b']},
    }
    """,
    )


def test_search_class():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "a": {"type": "fulltext+keyword"},
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
        os.path.join("test", "services", "records", "search.py")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from . import facets

def _(x):
    \"""Identity function for string extraction.\"""
    return x

class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facets = {
      'a_keyword': facets.a_keyword,
      'b': facets.b,
      '_id': facets._id,
      'created': facets.created,
      'updated': facets.updated,
      '_schema': facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }
    """,
    )
