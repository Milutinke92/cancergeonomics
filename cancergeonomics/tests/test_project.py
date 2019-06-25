from urllib.parse import urljoin

from cancergeonomics.resources.project import ProjectResource


def test_project_list(http_client, mocked_request):
    mocked_data = {"items": [{"name": "project_1"}]}
    mocked_url = urljoin(http_client.api, 'projects')
    mocked_request.get(mocked_url, json=mocked_data)
    project = ProjectResource(api_client=http_client)

    data = project.list()

    assert data == mocked_data['items']
