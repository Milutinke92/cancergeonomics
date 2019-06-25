from unittest.mock import PropertyMock

import faker as faker
import pytest
import requests_mock
from pytest_mock import mocker

from cancergeonomics.http.client import CGCBaseHttpClient
from cancergeonomics.resources.file import FileResource

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


@pytest.fixture()
def get_download_url():
    return generator.url() + "file.png"

@pytest.fixture
def file_resource(mocker, get_download_url):
    mocker.patch.object(FileResource, 'get_download_url', return_value=get_download_url)
    # mocker.return_value = get_download_url
    return mocker