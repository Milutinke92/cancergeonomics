import faker as faker
import pytest
import requests_mock

from cancergeonomics.http.client import CGCBaseHttpClient

generator = faker.Factory.create()


@pytest.fixture()
def http_client(mocked_request):
    client = CGCBaseHttpClient(token=generator.uuid4(), api=generator.url())
    return client


@pytest.fixture
def mocked_request(request):
    """
    :param request: pytest request object for cleaning up.
    :return: Returns instance of requests mocker used to mock HTTP calls.
    """
    m = requests_mock.Mocker()
    m.start()
    request.addfinalizer(m.stop)
    return m
