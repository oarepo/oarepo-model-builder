
import os
import re


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
                    "c": "fulltext"
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
                            "e": "fulltext"
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
                        "type": "nested",
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
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
        \"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet




b_nes_c = NestedLabeledFacet(path ="b_nes", nested_facet=TermsFacet(field = "b_nes.c"))



b_nes_d_keyword = NestedLabeledFacet(path ="b_nes", nested_facet=TermsFacet(field = "b_nes.d.keyword"))



b_nes_f_g = NestedLabeledFacet(path ="b_nes", nested_facet=TermsFacet(field = "b_nes.f.g"))



b_obj_c = TermsFacet(field = "b_obj.c")



b_obj_d_keyword = TermsFacet(field = "b_obj.d.keyword")



b_obj_f_g = NestedLabeledFacet(path ="b_obj.f", nested_facet=TermsFacet(field = "b_obj.f.g"))



_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
""",
    )

def test_array():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {

                    "a[]": "keyword",
                    "b[]": "fulltext",
                    "c[]": "fulltext+keyword"
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




a = TermsFacet(field = "a")



c_keyword = TermsFacet(field = "c.keyword")


_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
""",
    )

def test_array_nested():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "obj": {
                        "type": "object",
                        "properties": {
                            "arr": {
                                "type": "array",
                                "items": {
                                    "type": "nested",
                                    "properties": {
                                        "d": {"type": "keyword"},
                                        "e": {
                                            "type": "object",
                                            "properties": {
                                                "f": "keyword"
                                            }
                                        }

                                    }
                                }

                            }
                        }

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


obj_arr_d = NestedLabeledFacet(path ="obj.arr", nested_facet=TermsFacet(field = "obj.arr.d"))

obj_arr_e_f = NestedLabeledFacet(path ="obj.arr", nested_facet=TermsFacet(field = "obj.arr.e.f"))


_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
""",
    )

def test_top_facets():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "searchable": False,
                "properties": {
                    "a":  {"type": "fulltext+keyword",
                           "facets": {"searchable": True}},
                    "b": {
                        "type": "keyword",
                        "facets": {"field": 'TermsFacet(field="cosi")'},
                    },
                    "c": "keyword",
                    "arr": {
                        "type": "array",
                        "facets": {"searchable": True},
                        "items": {
                            "type": "nested",
                            "properties": {
                                "d": {"type": "keyword"},
                                "e": {
                                    "type": "object",
                                    "properties": {
                                        "f": "keyword"
                                    }
                                }

                            }
                        }

                    },
                    "lst2": {
                        "type": "array",
                        "items": {"type": "keyword"},
                        "facets": {"field": 'TermsFacet(field="cosi")'}
                    },
                    "lst[]": "keyword",
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



a_keyword = TermsFacet(field = "a.keyword")



b = TermsFacet(field="cosi")



arr_d = NestedLabeledFacet(path ="arr", nested_facet=TermsFacet(field = "arr.d"))

arr_e_f = NestedLabeledFacet(path ="arr", nested_facet=TermsFacet(field = "arr.e.f"))

lst2 = TermsFacet(field="cosi")

_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")

    """,
    )


def test_searchable_true():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "a":  {"type": "fulltext+keyword",
                           "facets": {"searchable": False}},
                    "b": {
                        "type": "keyword",
                        "facets": {"field": 'TermsFacet(field="cosi")'},
                    },
                    "c": "fulltext",
                    "f": {
                                "type" : "object",
                                "facets": {"searchable": False},
                                "properties": {"g": {"type": "keyword"}},

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
    print(data)

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet




b = TermsFacet(field="cosi")


_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")

    """,
    )