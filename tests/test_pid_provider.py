import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem


def clear_whitespaces(st):
    return re.sub(r"\s", "", st)


def get_sources(model_name, model_content=None):
    if not model_content:
        model_content = {
            "record": {"use": "invenio", "module": {"qualified": model_name}},
        }
    schema = load_model(
        f"{model_name}.yaml",
        model_content=model_content,
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(os.path.join(model_name, "records", "api.py")).read()
    return data


def test_simple():
    data = get_sources("test")
    data = clear_whitespaces(data)
    test_1 = """
    class TestIdProvider(RecordIdProviderV2 ):
        pid_type = "test"
    """
    test_2 = """
    pid = PIDField(
        provider=TestIdProvider,
        context_cls=PIDFieldContext,
        create=True
    )
    """
    assert clear_whitespaces(test_1) in data
    assert clear_whitespaces(test_2) in data


def test_over_six_characters():
    data = get_sources("test_lalaa")
    test_1 = """
    class TestLalaaIdProvider(RecordIdProviderV2 ):
        pid_type = "tstll"
    """
    test_2 = """
    pid = PIDField(
        provider=TestLalaaIdProvider,
        context_cls=PIDFieldContext,
        create=True
    )
    """
    assert clear_whitespaces(test_1) in clear_whitespaces(data)
    assert clear_whitespaces(test_2) in clear_whitespaces(data)


def test_over_six_characters_after_wovel_pruning():
    data = get_sources("test_lalaalalalalara")
    data = clear_whitespaces(data)
    test_1 = """
    class TestLalaalalalalaraIdProvider(RecordIdProviderV2 ):
        pid_type = "tstllr"
    """
    test_2 = """
    pid = PIDField(
        provider=TestLalaalalalalaraIdProvider,
        context_cls=PIDFieldContext,
        create=True
    )
    """
    assert clear_whitespaces(test_1) in data
    assert clear_whitespaces(test_2) in data


def test_import():
    model_content = {
        "record": {
            "use": "invenio",
            "module": {"qualified": "test"},
            "pid": {
                "provider-class": "MyVeryImportantCustomPidProvider",
                "generate": False,
                "imports": [
                    {"import": "custom.pid_provider.MyVeryImportantCustomPidProvider"}
                ],
            },
        },
    }
    data = get_sources("test", model_content=model_content)
    data = clear_whitespaces(data)

    assert (
        clear_whitespaces(
            """
    from custom.pid_provider import MyVeryImportantCustomPidProvider
    """
        )
        in data
    )

    assert (
        clear_whitespaces(
            """
        pid = PIDField(
        provider=MyVeryImportantCustomPidProvider,
        context_cls=PIDFieldContext,
        create=True 
    )
    """
        )
        in data
    )


def test_custom_type():
    model_content = {
        "record": {
            "use": "invenio",
            "pid": {"type": "it_must_be_named_like_this"},
            "module": {"qualified": "test"},
        },
    }
    data = get_sources("test", model_content=model_content)
    data = clear_whitespaces(data)

    test_1 = """
    class TestIdProvider(RecordIdProviderV2):
        pid_type = "it_must_be_named_like_this"
    """

    assert clear_whitespaces(test_1) in data
