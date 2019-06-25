import io
from unittest import mock
from unittest.mock import PropertyMock
from urllib.parse import urljoin

import faker

from cancergeonomics.resources.file import FileResource

generator = faker.Factory.create()
fake = faker.Faker()


def test_file_list(http_client, mocked_request):
    project_id = fake.text(10)
    mocked_data = {"items": [{"name": "file_1"}]}
    mocked_url = urljoin(http_client.api, f'files?{project_id}')
    mocked_request.get(mocked_url, json=mocked_data)
    file = FileResource(api_client=http_client)

    data = file.list(project_id)

    assert data == mocked_data['items']


def test_file_stat(http_client, mocked_request):
    file_id = fake.text(10)
    mocked_data = {"name": "file_1"}
    mocked_url = urljoin(http_client.api, f'files/{file_id}')
    mocked_request.get(mocked_url, json=mocked_data)
    file = FileResource(api_client=http_client)

    data = file.stat(file_id)

    assert data == mocked_data


def test_filed_download_info(http_client, mocked_request):
    file_id = fake.text(10)
    mocked_url_download = generator.url()
    mocked_url_info = urljoin(http_client.api, f'files/{file_id}/download_info')
    mocked_request.get(mocked_url_info, json={"url": mocked_url_download})

    file = FileResource(api_client=http_client)

    url = file.get_download_url(file_id)

    assert url == mocked_url_download


def test_file_download(http_client, mocked_request, get_download_url, file_resource):
    file_id = fake.text(10)
    file_path = "/tmp/test.png"
    mocked_file = io.BytesIO(b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01")
    mocked_file_content = mocked_file.read()
    mocked_request.get(
        get_download_url, content=mocked_file_content, headers={"Content-Type": "application/octet-stream"}
    )
    mocked_request.head(
        get_download_url, headers={"Content-Type": "application/octet-stream"}
    )

    file = FileResource(api_client=http_client)

    file_path_saved = file.download(file_id, file_path)

    assert file_path_saved == file_path

    with open(file_path_saved, 'rb') as f:
        content = f.read()
        assert content == mocked_file_content


