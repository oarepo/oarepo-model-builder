import json
import os
import re
from io import StringIO
from pathlib import Path
from typing import Dict

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import AbstractFileSystem

# from tests.mock_filesystem import MockFilesystem


class MockFilesystem(AbstractFileSystem):
    def __init__(self):
        self.files: Dict[str, StringIO] = {}

    def open(self, path: str, mode: str = "r"):
        path = Path(path).absolute()
        if mode == "r":
            if not path in self.files:
                raise FileNotFoundError(f"File {path} not found. Known files {[f for f in self.files]}")
            return StringIO(self.files[path].getvalue())
        self.files[path] = StringIO()
        self.files[path].close = lambda: None
        return self.files[path]

    def exists(self, path):
        path = Path(path).absolute()
        return path in self.files

    def mkdir(self, path):
        pass

    def snapshot(self):
        ret = {}
        for fname, io in self.files.items():
            ret[fname] = io.getvalue()
        return ret


def test_include_invenio():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "oarepo:use": "invenio",
            "model": {
                "properties": {
                    "a": {"type": "fulltext+keyword"},
                    "b": {"type": "keyword", "oarepo:facets": {"field": 'TermsFacet(field="cosi")'}},
                }
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "facets.py")).read()
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from elasticsearch_dsl import Facet
from elasticsearch_dsl.query import Nested

class NestedLabeledFacet(Facet):
    agg_type = "nested"

    def __init__(self, path, nested_facet, label = ''):
        self._path = path
        self._inner = nested_facet
        self._label = label
        super(NestedLabeledFacet, self).__init__(
            path=path,  aggs={"inner": nested_facet.get_aggregation(),}
        )

    def get_values(self, data, filter_values):
        return self._inner.get_values(data.inner, filter_values)

    def add_filter(self, filter_values):
        inner_q = self._inner.add_filter(filter_values)
        if inner_q:
            return Nested(path=self._path, query=inner_q)

    def get_labelled_values(self, data, filter_values):
        \"""Get a labelled version of a bucket.\"""
        try:
            out = data['buckets']
        except:
            out = []
        return {'buckets': out, 'label': str(self._label)}



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
        "test.yaml",
        "test",
        model_content={
            "oarepo:use": "invenio",
            "model": {
                "properties": {
                    "b": {
                        "properties": {
                            "c": {
                                "type": "keyword",
                            },
                            "d": {"type": "fulltext+keyword"},
                            "f": {
                                "properties": {"g": {"type": "keyword"}},
                                "oarepo:mapping": {"type": "nested"},
                                "oarepo:marshmallow": {"class": "nest.f.F", "generate": True},
                            },
                        },
                        "oarepo:mapping": {"type": "nested"},
                        "oarepo:marshmallow": {"class": "nest.b.B", "generate": True},
                    }
                }
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "facets.py")).read()
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from elasticsearch_dsl import Facet
from elasticsearch_dsl.query import Nested

class NestedLabeledFacet(Facet):
    agg_type = "nested"

    def __init__(self, path, nested_facet, label = ''):
        self._path = path
        self._inner = nested_facet
        self._label = label
        super(NestedLabeledFacet, self).__init__(
            path=path,  aggs={\"inner\": nested_facet.get_aggregation(),}
        )

    def get_values(self, data, filter_values):
        return self._inner.get_values(data.inner, filter_values)

    def add_filter(self, filter_values):
        inner_q = self._inner.add_filter(filter_values)
        if inner_q:
            return Nested(path=self._path, query=inner_q)

    def get_labelled_values(self, data, filter_values):
        \"""Get a labelled version of a bucket.\"""
        try:
            out = data['buckets']
        except:
            out = []
        return {'buckets': out, 'label': str(self._label)}



b_c = NestedLabeledFacet(path = \"b\" , nested_facet =TermsFacet(field = \"b.c\"))



b_d_keyword = NestedLabeledFacet(path = \"b\" , nested_facet =TermsFacet(field = \"b.d.keyword\"))



b_f_g = NestedLabeledFacet(path = \"b\", nested_facet = NestedLabeledFacet(path = "b.f" , nested_facet =TermsFacet(field = "b.f.g")))



_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
    """,
    )


def test_search_class():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "oarepo:use": "invenio",
            "model": {
                "properties": {
                    "a": {"type": "fulltext+keyword"},
                    "b": {"type": "keyword", "oarepo:facets": {"field": 'TermsFacet(field="cosi")'}},
                }
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "search.py")).read()
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from . import facets



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
    """,
    )
