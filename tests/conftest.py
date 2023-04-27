import pytest


@pytest.fixture(autouse=True)
def clear_datatypes():
    from oarepo_model_builder.datatypes import datatypes

    datatypes._clear_caches()


def pytest_configure():
    pass
    # logging.basicConfig(level=logging.ERROR)
    # logger = logging.getLogger("oarepo_model_builder.cst")
    # logger.setLevel(logging.DEBUG)
