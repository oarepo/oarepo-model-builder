import os

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem
from tests.utils import strip_whitespaces

DUMMY_YAML = "test.yaml"


def test_sort():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a": {
                        "type": "fulltext+keyword",
                        "sortable": {"key": "a_test"},
                    },
                    "b": {
                        "type": "keyword",
                        "facets": {
                            "field": 'TermsFacet(field="cosi")',
                            "facet-groups": ["curator"],
                        },
                        "sortable": {"key": "b_test", "order": "desc"},
                    },
                    "c": {
                        "type": "object",
                        "properties": {
                            "d": {"type": "keyword", "sortable": {"order": "desc"}}
                        },
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
        os.path.join("test", "services", "records", "search.py")
    ).read()
    print(data)
    assert strip_whitespaces(data) == strip_whitespaces(
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from flask_babelex import lazy_gettext as _
from . import facets


class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facet_groups ={
        
            'curator': {
                
                    'b' : facets.b,

                
            
                **getattr(InvenioSearchOptions, 'facet_groups', {}).get('curator', {})
            
            },
        
    }

    facets = {


    'b': facets.b,



    'c_d': facets.c_d,



    **getattr(InvenioSearchOptions, 'facets', {})

    }


    sort_options = {
        
            
                **InvenioSearchOptions.sort_options,
            

        


    'a_test': {'fields': ['a']},



    'b_test': {'fields': ['-b']},



    'c_d': {'fields': ['-c.d']},


    }
    """,
    )


def test_search_class():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a": {"type": "fulltext+keyword"},
                    "b": {
                        "type": "keyword",
                        "facets": {"field": "cosi"},
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
        os.path.join("test", "services", "records", "search.py")
    ).read()
    print(data)
    assert strip_whitespaces(data) == strip_whitespaces(
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from flask_babelex import lazy_gettext as _
from . import facets


class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facet_groups ={
        
    }

    facets = {

    'b': facets.b,

    **getattr(InvenioSearchOptions, 'facets', {})

    }
    """,
    )


def test_search_options_base_class():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "search-options": {
                    "base-classes": ["BaseSearchOptions"],
                    "imports": [{"import": "blah.BaseSearchOptions"}],
                },
                "properties": {},
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
        os.path.join("test", "services", "records", "search.py")
    ).read()
    print(data)
    assert strip_whitespaces(data) == strip_whitespaces(
        """
from blah import BaseSearchOptions
from flask_babelex import lazy_gettext as _
from . import facets


class TestSearchOptions(BaseSearchOptions):
    \"""TestRecord search options.\"""

    facet_groups ={
        
    }

    facets = {


    **getattr(BaseSearchOptions, 'facets', {})

    }
    """,
    )


def test_facet_groups():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "search-options": {
                    "base-classes": ["BaseSearchOptions"],
                    "imports": [{"import": "blah.BaseSearchOptions"}],
                },
                "properties": {
                    "a": {
                        "type": "keyword",
                        "facets": {"facet-groups": ["curator", "user"]},
                    },
                    "b": {
                        "type": "keyword",
                        "facets": {"searchable": True, "facet-groups": []},
                    },
                    "b2": {
                        "type": "keyword",
                        "facets": {"searchable": True},
                    },
                    "b3": {
                        "type": "keyword",
                        "facets": {"searchable": True, "facet-groups": ['default']},
                    },
                    "c": {
                        "type": "keyword",
                        "facets": {"searchable": True, "facet": False},
                    },
                    "d": {"type": "keyword", "facets": {"searchable": False}},
                    "g": {
                        "type": "array",
                        "items": {
                            "type": "keyword",
                            "facets": {"facet-groups": ["curator"]},
                        },
                    },
                    "arr": {
                        "type": "array",
                        "facets": {"searchable": True},
                        "items": {
                            "type": "nested",
                            "properties": {
                                "d": {"type": "keyword", "facets": {"facet": False}},
                                "e": {
                                    "type": "object",
                                    "properties": {
                                        "f": "keyword",
                                    },
                                },
                            },
                        },
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
        os.path.join("test", "services", "records", "search.py")
    ).read()
    print(data)
    data2 = builder.filesystem.open(
        os.path.join("test", "services", "records", "facets.py")
    ).read()
    print(data2)
    data3 = builder.filesystem.read(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    )
    import json

    data3 = json.loads(data3)
    print(data3)
    assert strip_whitespaces(data) == strip_whitespaces(
        """
from blah import BaseSearchOptions
from flask_babelex import lazy_gettext as _
from . import facets


class TestSearchOptions(BaseSearchOptions):
    \"""TestRecord search options.\"""

    facet_groups ={
        
            'curator': {
                
                    'a' : facets.a,

                
                    'g' : facets.g,

                
            
                **getattr(BaseSearchOptions, 'facet_groups', {}).get('curator', {})
            
            },
        
            'user': {
                
                    'a' : facets.a,

                
            
                **getattr(BaseSearchOptions, 'facet_groups', {}).get('user', {})
            
            },
        
            'default': {
                
                    'b3' : facets.b3,

                
            
                **getattr(BaseSearchOptions, 'facet_groups', {}).get('default', {})
            
            },
        
    }

    facets = {


    'a': facets.a,



    'arr_e_f': facets.arr_e_f,



    'b2': facets.b2,



    'b3': facets.b3,



    'g': facets.g,



    **getattr(BaseSearchOptions, 'facets', {})

    }
    """,
    )


def test_replace_sort_options():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "search-options": {"sort-options-field": "extra_sort_options"},
                "properties": {
                    "a": {
                        "type": "keyword",
                        "sortable": {"key": "a_test"},
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
        os.path.join("test", "services", "records", "search.py")
    ).read()
    print(data)
    assert strip_whitespaces(data) == strip_whitespaces(
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from flask_babelex import lazy_gettext as _
from . import facets


class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facet_groups ={
    }

    facets = {
    'a': facets.a,
    **getattr(InvenioSearchOptions, 'facets', {})
    }
    extra_sort_options = {
                **InvenioSearchOptions.extra_sort_options,
                'a_test': {'fields': ['a']},
    }
    """,
    )
