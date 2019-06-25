class Resource(object):
    RESOURCE_ROOT_URL = NotImplemented

    def __init__(self, api_client):
        self.api_client = api_client

    def get(self, id):
        return self.api_client.get(self.detail_url(id))

    def filter(self, query_params=None):
        return self.api_client.get(self.RESOURCE_ROOT_URL, query_params=query_params)['items']

    def update(self, id, data):
        return self.api_client.patch(self.detail_url(id), data=data)

    def detail_url(self, id):
        return self.RESOURCE_ROOT_URL.rstrip('/') + f"/{id}"
