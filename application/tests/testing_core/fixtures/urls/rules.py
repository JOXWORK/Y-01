import pytest

from tests.testing_core.test_depends import test_depends


class UrlRules:
    create = test_depends.urls.rules("/create")
    get = test_depends.urls.rules("/get")
    delete = test_depends.urls.rules("/delete")


@pytest.fixture(scope="class")
def url_rules():
    return UrlRules()
