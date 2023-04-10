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
                    "jej": {
                        "type": "nested",
                        "properties": {
                            "c": {
                                "type": "keyword",
                                "facets": {"field": 'TermsFacet(field="cosi")'},
                            }
                        },
                    },
                    "a": "fulltext+keyword",
                    "b": {
                        "type": "keyword",
                        "facets": {"field": 'TermsFacet(field="cosi")'},
                    },
                    "c": "fulltext",
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



jej_c = NestedLabeledFacet(path ="jej", nested_facet = TermsFacet(field="cosi"))



a_keyword = TermsFacet(field="a.keyword", label=_("a/keyword.label") )



b = TermsFacet(field="cosi")



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )


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
                                "type": "nested",
                                "properties": {"g": {"type": "keyword"}},
                            },
                        },
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



b_c = NestedLabeledFacet(path ="b", nested_facet = TermsFacet(field="b.c", label=_("b/c.label") ))



b_d_keyword = NestedLabeledFacet(path ="b", nested_facet = TermsFacet(field="b.d.keyword", label=_("b/d/keyword.label") ))



b_f_g = NestedLabeledFacet(path ="b", nested_facet = NestedLabeledFacet(path ="b.f", nested_facet = TermsFacet(field="b.f.g", label=_("b/f/g.label") )))



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )

""",
    )


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
                                "type": "object",
                                "properties": {"g": {"type": "keyword"}},
                            },
                            "e": "fulltext",
                        },
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet



b_c = TermsFacet(field="b.c", label=_("b/c.label") )



b_d_keyword = TermsFacet(field="b.d.keyword", label=_("b/d/keyword.label") )



b_f_g = TermsFacet(field="b.f.g", label=_("b/f/g.label") )



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )
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
                                "type": "object",
                                "properties": {"g": {"type": "keyword"}},
                            },
                        },
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
                        },
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



b_nes_c = NestedLabeledFacet(path ="b_nes", nested_facet = TermsFacet(field="b_nes.c", label=_("b_nes/c.label") ))



b_nes_d_keyword = NestedLabeledFacet(path ="b_nes", nested_facet = TermsFacet(field="b_nes.d.keyword", label=_("b_nes/d/keyword.label") ))



b_nes_f_g = NestedLabeledFacet(path ="b_nes", nested_facet = TermsFacet(field="b_nes.f.g", label=_("b_nes/f/g.label") ))



b_obj_c = TermsFacet(field="b_obj.c", label=_("b_obj/c.label") )



b_obj_d_keyword = TermsFacet(field="b_obj.d.keyword", label=_("b_obj/d/keyword.label") )



b_obj_f_g = NestedLabeledFacet(path ="b_obj.f", nested_facet = TermsFacet(field="b_obj.f.g", label=_("b_obj/f/g.label") ))



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )
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
                    "c[]": "fulltext+keyword",
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet



a = TermsFacet(field="a", label=_("a.label") )



c_keyword = TermsFacet(field="c.keyword", label=_("c/keyword.label") )



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )
""",
    )


def test_array_object():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "arr": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "a": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {"c": "keyword"},
                                    },
                                }
                            },
                        },
                    },
                    "test": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "keyword"}},
                    },
                    "test2": {
                        "type": "array",
                        "items": {
                            "type": "nested",
                            "properties": {"g": {"type": "keyword"}},
                        },
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



arr_a_c = TermsFacet(field="arr.a.c", label=_("arr/a/c.label") )



test = TermsFacet(field="test", label=_("test.label") )



test2_g = NestedLabeledFacet(path ="test2", nested_facet = TermsFacet(field="test2.g", label=_("test2/g.label") ))



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )
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
                                        "d": {
                                            "type": "fulltext+keyword",
                                            # "facets": {"key": "test"},
                                        },
                                        "e": {
                                            "type": "object",
                                            "properties": {"f": "keyword"},
                                        },
                                    },
                                },
                            }
                        },
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



obj_arr_d_keyword = NestedLabeledFacet(path ="obj.arr", nested_facet = TermsFacet(field="obj.arr.d.keyword", label=_("obj/arr/d/keyword.label") ))



obj_arr_e_f = NestedLabeledFacet(path ="obj.arr", nested_facet = TermsFacet(field="obj.arr.e.f", label=_("obj/arr/e/f.label") ))



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )
""",
    )


def test_not_searchable():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "a": {"type": "fulltext+keyword", "facets": {"searchable": False}},
                    "b": {
                        "type": "keyword",
                        "facets": {"field": 'TermsFacet(field="cosi")'},
                    },
                    "arr": {
                        "type": "array",
                        "items": {
                            "type": "nested",
                            "properties": {
                                "d": {
                                    "type": "keyword",
                                    "facets": {"searchable": False},
                                },
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



b = TermsFacet(field="cosi")



arr_e_f = NestedLabeledFacet(path ="arr", nested_facet = TermsFacet(field="arr.e.f", label=_("arr/e/f.label") ))



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )

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
                    "a": {"type": "fulltext+keyword", "facets": {"searchable": True}},
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
                                        "f": "keyword",
                                    },
                                },
                            },
                        },
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

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



a_keyword = TermsFacet(field="a.keyword", label=_("a/keyword.label") )



b = TermsFacet(field="cosi")



arr_d = NestedLabeledFacet(path ="arr", nested_facet = TermsFacet(field="arr.d", label=_("arr/d.label") ))



arr_e_f = NestedLabeledFacet(path ="arr", nested_facet = TermsFacet(field="arr.e.f", label=_("arr/e/f.label") ))



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )

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
                    "a": {"type": "fulltext+keyword", "facets": {"searchable": False}},
                    "b": {
                        "type": "keyword",
                        "facets": {"field": 'TermsFacet(field="cosi")'},
                    },
                    "c": "fulltext",
                    "f": {
                        "type": "object",
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

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet



b = TermsFacet(field="cosi")



_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )

    """,
    )


def test_enum():
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "model": {
                "use": "invenio",
                "properties": {
                    "a": {"type": "keyword", "enum": ["a", "b"]},
                    "b": {
                        "type": "keyword",
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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.enum import EnumTermsFacet


a = EnumTermsFacet(field="a", label=_("a.label") )



b = TermsFacet(field="b", label=_("b.label") )


_id = TermsFacet(field="id", label=_("id.label") )



created = DateTimeFacet(field="created", label=_("created.label") )



updated = DateTimeFacet(field="updated", label=_("updated.label") )



_schema = TermsFacet(field="$schema", label=_("$schema.label") )

    """,
    )
