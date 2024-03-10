import pytest

from oarepo_model_builder.loaders import json_loader, yaml_loader


@pytest.fixture(autouse=True)
def clear_datatypes():
    from oarepo_model_builder.datatypes import datatypes

    datatypes._clear_caches()


@pytest.fixture
def loaders():
    return {
        "json": json_loader,
        "json5": json_loader,
        "yaml": yaml_loader,
        "yml": yaml_loader,
    }
