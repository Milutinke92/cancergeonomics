import io
import sys
import faker

if sys.version_info[0] >= 3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

generator = faker.Factory.create()
fake = faker.Faker()


def test_file_list(http_client, mocked_request):
    """
    Test retrieving list of files in project by project_id
    :param http_client: Mocked APIClient instance
    :param mocked_request: mocked_request instance
    """
    project_id = fake.text(10)
    mocked_data = {"items": [{"name": "file_1"}]}
    mocked_url = urljoin(http_client.api, 'files?{}'.format(project_id))
    mocked_request.get(mocked_url, json=mocked_data)

    data = http_client.file.list(project_id)

    assert data == mocked_data['items']


def test_file_stat(http_client, mocked_request):
    """
    Test retrieving file details by file_id
    :param http_client: Mocked APIClient instance
    :param mocked_request: mocked_request instance
    """
    file_id = fake.text(10)
    mocked_data = {"name": "file_1"}
    mocked_url = urljoin(http_client.api, 'files/{}'.format(file_id))
    mocked_request.get(mocked_url, json=mocked_data)

    data = http_client.file.stat(file_id)

    assert data == mocked_data


def test_file_download_info(http_client, mocked_request):
    """
    Test getting Download url for File  by file_id
    :param http_client: Mocked APIClient instance
    :param mocked_request: mocked_request instance
    """
    file_id = fake.text(10)
    mocked_url_download = generator.url()
    mocked_url_info = urljoin(http_client.api, 'files/{}/download_info'.format(file_id))
    mocked_request.get(mocked_url_info, json={"url": mocked_url_download})

    url = http_client.file.get_download_url(file_id)

    assert url == mocked_url_download


def test_file_download(http_client, mocked_request, get_download_url, file_resource):
    """
    Test downloading file by file_id and storing to some destination
    :param http_client: Mocked APIClient instance
    :param mocked_request: mocked_request instance
    :param get_download_url: URL
    :param mocked_request: MockedFixture instance with mocked FileResource methods
    """
    file_id = fake.text(10)
    file_path = "/tmp/test.png"
    mocked_file = io.BytesIO(b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01")
    mocked_file_content = mocked_file.read()
    mocked_request.get(
        get_download_url, content=mocked_file_content,
        headers={"Content-Type": "application/octet-stream"}
    )
    mocked_request.head(
        get_download_url, headers={"Content-Type": "application/octet-stream"}
    )

    file_path_saved = http_client.file.download(file_id, file_path)

    assert file_path_saved == file_path

    with open(file_path_saved, 'rb') as f:
        content = f.read()
        assert content == mocked_file_content
