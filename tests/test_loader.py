from oarepo_model_builder.schema.loader import SchemaLoader
from oarepo_model_builder.schema.value import ReferenceType, Source


def test_simple_loader(loaders):
    loader = SchemaLoader(loaders, {})
    data = loader.load(
        Source.create("simple.json", ReferenceType.NONE, content={"a": 1})
    )
    assert data.dump() == {"a": 1}


def test_include(loaders):
    loader = SchemaLoader(loaders, {"incl": lambda x: {"a": 1}})
    data = loader.load(
        Source.create("include.json", ReferenceType.NONE, content={"$ref": "incl"})
    )
    assert data.dump() == {"a": 1}
    assert len(data["a"].source) == 2

    data = loader.load(
        Source.create("include.json", ReferenceType.NONE, content={"use": "incl"})
    )
    assert data.dump() == {"a": 1}
    assert data.source.reference_type == ReferenceType.NONE
    assert data["a"].source.reference_type == ReferenceType.USE

    data = loader.load(
        Source.create("include.json", ReferenceType.NONE, content={"extend": "incl"})
    )
    assert data.dump() == {"a": 1}
    assert data["a"].source.reference_type == ReferenceType.EXTEND


def test_double_include(loaders):
    loader = SchemaLoader(
        loaders, {"incl": lambda x: {"a": 1}, "incl1": lambda x: {"a": {"use": "incl"}}}
    )
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"b": {"$ref": "incl1"}}
        )
    )
    assert data.dump() == {"b": {"a": {"a": 1}}}


def test_override(loaders):
    loader = SchemaLoader(loaders, {"incl": lambda x: {"a": 1}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": 2}
        )
    )
    assert data.dump() == {"a": 2}


def test_merge_arrays(loaders):
    loader = SchemaLoader(loaders, {"incl": lambda x: {"a": [1, 2]}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # prepend
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "<a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # append
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", ">a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}

    # included says append
    loader = SchemaLoader(loaders, {"incl": lambda x: {">a": [1, 2]}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # included says append, including prepend
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "<a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # included says append, including append => including wins
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", ">a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}

    # included says prepend
    loader = SchemaLoader(loaders, {"incl": lambda x: {"<a": [1, 2]}})
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}

    # included says prepend, including prepend => including wins
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", "<a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [3, 4, 1, 2]}

    # included says prepend, including append
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"$ref": "incl", ">a": [3, 4]}
        )
    )
    assert data.dump() == {"a": [1, 2, 3, 4]}


def test_extend_use(loaders):
    loader = SchemaLoader(
        loaders,
        {
            "incl": lambda x: {"a": 1, "b": 2},
            "incl1": lambda x: {"use": "incl", "d": 4},
        },
    )
    data = loader.load(
        Source.create(
            "include.json", ReferenceType.NONE, content={"extend": "incl1", "a": 3}
        )
    )
    assert data.dump() == {"a": 3, "b": 2, "d": 4}
    assert data["a"].source.reference_type == ReferenceType.NONE
    assert data["b"].source.reference_type == ReferenceType.USE
    assert data["b"].source.previous.reference_type == ReferenceType.EXTEND
    assert data["d"].source.reference_type == ReferenceType.EXTEND
