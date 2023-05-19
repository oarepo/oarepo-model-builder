import pytest


@pytest.fixture(autouse=True)
def clear_datatypes():
    from oarepo_model_builder.datatypes import datatypes

    datatypes._clear_caches()
