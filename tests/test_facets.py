import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

DUMMY_YAML = "test.yaml"


def test_include_invenio():
    schema = load_model(
        "test.yaml",
        model_content={
            "record": {
                "use": "invenio",
                "module" : {"qualified": "test"},
                "properties": {
                    "jej": {
                        "type": "nested",
                        "properties": {
                            "c": {
                                "type": "keyword",
                                "facets": {"path": "cosi"},
                            }
                        },
                    },
                    "a": "fulltext+keyword",
                    "b": {
                        "type": "keyword",
                        "facets": {
                            "path": "cosi",
                            "imports": [
                                {
                                    "import": "invenio_records_resources.services.records.facets.TermsFacet2"
                                }
                            ],
                        },
                    },
                    "c": "fulltext",
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
from invenio_records_resources.services.records.facets import TermsFacet2

from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



_schema = TermsFacet(field="$schema", label=_("$schema.label") )



a_keyword = TermsFacet(field="a.keyword", label=_("a/keyword.label") )



b = TermsFacet(field="b.cosi", label =_("b.label"))



created = DateTimeFacet(field="created", label=_("created.label") )



_id = TermsFacet(field="id", label=_("id.label") )



jej_c = NestedLabeledFacet(path ="jej", nested_facet = TermsFacet(field="jej.c.cosi", label =_("jej/c.label")))



updated = DateTimeFacet(field="updated", label=_("updated.label") )




    """,
    )


def test_nested():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

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

_schema = TermsFacet(field="$schema", label=_("$schema.label") )

b_c = NestedLabeledFacet(path ="b", nested_facet = TermsFacet(field="b.c", label=_("b/c.label") ))



b_d_keyword = NestedLabeledFacet(path ="b", nested_facet = TermsFacet(field="b.d.keyword", label=_("b/d/keyword.label") ))



b_f_g = NestedLabeledFacet(path ="b", nested_facet = NestedLabeledFacet(path ="b.f", nested_facet = TermsFacet(field="b.f.g", label=_("b/f/g.label") )))

created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )







updated = DateTimeFacet(field="updated", label=_("updated.label") )





""",
    )


def test_object():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
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
                                "properties": {
                                    "g": {"type": "keyword", "facets": {"path": "cosi"}}
                                },
                            },
                            "e": "fulltext",
                        },
                    }
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

_schema = TermsFacet(field="$schema", label=_("$schema.label") )

b_c = TermsFacet(field="b.c", label=_("b/c.label") )



b_d_keyword = TermsFacet(field="b.d.keyword", label=_("b/d/keyword.label") )



b_f_g = TermsFacet(field="b.f.g.cosi", label=_("b/f/g.label") )

created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )







updated = DateTimeFacet(field="updated", label=_("updated.label") )




""",
    )


def test_nest_obj():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

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


_schema = TermsFacet(field="$schema", label=_("$schema.label") )

b_nes_c = NestedLabeledFacet(path ="b_nes", nested_facet = TermsFacet(field="b_nes.c", label=_("b_nes/c.label") ))



b_nes_d_keyword = NestedLabeledFacet(path ="b_nes", nested_facet = TermsFacet(field="b_nes.d.keyword", label=_("b_nes/d/keyword.label") ))



b_nes_f_g = NestedLabeledFacet(path ="b_nes", nested_facet = TermsFacet(field="b_nes.f.g", label=_("b_nes/f/g.label") ))



b_obj_c = TermsFacet(field="b_obj.c", label=_("b_obj/c.label") )



b_obj_d_keyword = TermsFacet(field="b_obj.d.keyword", label=_("b_obj/d/keyword.label") )



b_obj_f_g = NestedLabeledFacet(path ="b_obj.f", nested_facet = TermsFacet(field="b_obj.f.g", label=_("b_obj/f/g.label") ))







created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )

updated = DateTimeFacet(field="updated", label=_("updated.label") )




""",
    )


def test_array():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a[]": "keyword",
                    "b[]": "fulltext",
                    "c[]": "fulltext+keyword",
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

_schema = TermsFacet(field="$schema", label=_("$schema.label") )

a = TermsFacet(field="a", label=_("a.label") )



c_keyword = TermsFacet(field="c.keyword", label=_("c/keyword.label") )







created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )

updated = DateTimeFacet(field="updated", label=_("updated.label") )




""",
    )


def test_array_object():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

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

_schema = TermsFacet(field="$schema", label=_("$schema.label") )

arr_a_c = TermsFacet(field="arr.a.c", label=_("arr/a/c.label") )



created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )

test = TermsFacet(field="test", label=_("test.label") )



test2_g = NestedLabeledFacet(path ="test2", nested_facet = TermsFacet(field="test2.g", label=_("test2/g.label") ))

updated = DateTimeFacet(field="updated", label=_("updated.label") )




""",
    )


def test_array_nested():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
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
                                            "facets": {"key": "test"},
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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

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

_schema = TermsFacet(field="$schema", label=_("$schema.label") )



created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )

test = NestedLabeledFacet(path ="obj.arr", nested_facet = TermsFacet(field="obj.arr.d.keyword", label=_("obj/arr/d/keyword.label") ))



obj_arr_e_f = NestedLabeledFacet(path ="obj.arr", nested_facet = TermsFacet(field="obj.arr.e.f", label=_("obj/arr/e/f.label") ))

updated = DateTimeFacet(field="updated", label=_("updated.label") )




""",
    )


def test_not_searchable():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a": {"type": "fulltext+keyword", "facets": {"searchable": False}},
                    "b": {
                        "type": "keyword",
                        "facets": {"path": "cosi"},
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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "record", ["record"], "")

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


_schema = TermsFacet(field="$schema", label=_("$schema.label") )






arr_e_f = NestedLabeledFacet(path ="arr", nested_facet = TermsFacet(field="arr.e.f", label=_("arr/e/f.label") ))

b = TermsFacet(field="b.cosi", label =_("b.label") )




created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )


updated = DateTimeFacet(field="updated", label=_("updated.label") )




    """,
    )


def test_top_facets():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "searchable": False,
                "properties": {
                    "a": {"type": "fulltext+keyword", "facets": {"searchable": True}},
                    "b": {
                        "type": "keyword",
                        "facets": {"field": "cosi"},
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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "record", ["record"], "")

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


_schema = TermsFacet(field="$schema", label=_("$schema.label") )


a_keyword = TermsFacet(field="a.keyword", label=_("a/keyword.label") )



arr_d = NestedLabeledFacet(path ="arr", nested_facet = TermsFacet(field="arr.d", label=_("arr/d.label") ))



arr_e_f = NestedLabeledFacet(path ="arr", nested_facet = TermsFacet(field="arr.e.f", label=_("arr/e/f.label") ))

created = DateTimeFacet(field="created", label=_("created.label") )


_id = TermsFacet(field="id", label=_("id.label") )






updated = DateTimeFacet(field="updated", label=_("updated.label") )




    """,
    )


def test_searchable_true():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a": {"type": "fulltext+keyword", "facets": {"searchable": False}},
                    "b": {
                        "type": "keyword",
                        "facets": {"path": "cosi"},
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
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "record", ["record"], "")
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


_schema = TermsFacet(field="$schema", label=_("$schema.label") )

b = TermsFacet(field="b.cosi", label =_("b.label"))


created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )


updated = DateTimeFacet(field="updated", label=_("updated.label") )




    """,
    )


def test_enum():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a": {
                        "type": "keyword",
                        "enum": ["a", "b"],
                        "facets": {
                            "facet-class": "EnumTermsFacet",
                            "imports": [
                                {"import": "oarepo_runtime.facets.enum.EnumTermsFacet"}
                            ],
                        },
                    },
                    "b": {
                        "type": "keyword",
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
from oarepo_runtime.facets.enum import EnumTermsFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label") )


a = EnumTermsFacet(field="a", label=_("a.label") )



b = TermsFacet(field="b", label=_("b.label") )





created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )


updated = DateTimeFacet(field="updated", label=_("updated.label") )




    """,
    )


def test_customizations_args_class():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a": {
                        "type": "keyword",
                        "facets": {
                            "facet-class": "MyFacetClass",
                            "args": ["blah=123"],
                            "imports": [{"import": "blah.MyFacetClass"}],
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

from blah import MyFacetClass
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label") )


a = MyFacetClass(field="a", label=_("a.label"), blah=123 )


created = DateTimeFacet(field="created", label=_("created.label") )


_id = TermsFacet(field="id", label=_("id.label") )






updated = DateTimeFacet(field="updated", label=_("updated.label") )




    """,
    )


def test_customizations_field():
    schema = load_model(
        DUMMY_YAML,
        model_content={
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "a": {
                        "type": "keyword",
                        "facets": {
                            "facet-class": "MyFacetClass",
                            "args": ["blah=123", 'alzp="jej"'],
                            "path": "aaa",
                            "imports": [{"import": "blah.MyFacetClass"}],
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

from blah import MyFacetClass

from invenio_records_resources.services.records.facets import TermsFacet

from oarepo_runtime.facets.date import DateTimeFacet


_schema = TermsFacet(field="$schema", label=_("$schema.label") )


a = MyFacetClass(field="a.aaa", label=_("a.label"), blah=123, alzp="jej" )





created = DateTimeFacet(field="created", label=_("created.label") )

_id = TermsFacet(field="id", label=_("id.label") )


updated = DateTimeFacet(field="updated", label=_("updated.label") )




    """,
    )
