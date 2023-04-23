import pytest


@pytest.fixture(autouse=True)
def clear_datatypes():
    from oarepo_model_builder.datatypes import datatypes

    datatypes._clear_caches()


@pytest.fixture(autouse=True)
def clear_validation():
    from oarepo_model_builder.validation import model_validator

    model_validator._clear_cache()


def pytest_configure():
    pass
    # logging.basicConfig(level=logging.ERROR)
    # logger = logging.getLogger("oarepo_model_builder.cst")
    # logger.setLevel(logging.DEBUG)
