import sys

if sys.version_info[0] >= 3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin


def test_project_list(http_client, mocked_request):
    """
    Test ProjectResource.list method
    :param http_client: Mocked APIClient instance
    :param mocked_request: mocked_request instance
    """
    mocked_data = {"items": [{"name": "project_1"}]}
    mocked_url = urljoin(http_client.api, 'projects')
    mocked_request.get(mocked_url, json=mocked_data)

    data = http_client.project.list()

    assert data == mocked_data['items']
