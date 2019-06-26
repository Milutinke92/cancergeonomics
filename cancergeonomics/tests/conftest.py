import faker as faker
import pytest
import requests_mock

from cancergeonomics.api_client import ApiClient
from cancergeonomics.resources.file import FileResource

generator = faker.Factory.create()


@pytest.fixture()
def http_client():
    """
    :return: CGCBaseHttpClient object with mocked token and api root url.
    """
    client = ApiClient(token=generator.uuid4(), api=generator.url())
    return client


@pytest.fixture
def mocked_request(request):
    """
    Mocked request which will be used for predefining responses
    :param request: pytest request object for cleaning up.
    :return: Returns instance of requests mocker.
    """
    m = requests_mock.Mocker()
    m.start()
    request.addfinalizer(m.stop)
    return m


@pytest.fixture()
def get_download_url():
    """
    Fixture to get random url for download file.
    :return: Mocked url as url to Download file
    """
    return generator.url() + "file.png"


@pytest.fixture
def file_resource(mocker, get_download_url):
    """
    Purpose of this fixture is to mock `get_download_url` method of FileResource
    :param mocker: MockFixture instance
    :param get_download_url: pytest fixture get_download_url
    :return: mocked FileResource with get_download_url method
    """
    mocker.patch.object(FileResource, 'get_download_url', return_value=get_download_url)
    return mocker
