from urllib.parse import urljoin

import faker

from cancergeonomics.resources.file import FileResource

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
